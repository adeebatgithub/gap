from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db import transaction
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, DeleteView, View

from academics.models import Session, Enrollment, Attendance
from timetable.models import TimetableCell


class SessionDetailView(PermissionRequiredMixin, DetailView):
    permission_required = ('academics.view_session', 'academics.view_attendance')
    model = Session
    template_name = 'teacher/sessions/detail.html'
    context_object_name = 'session'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "attendances": Attendance.objects.filter(session=self.object),
        })
        return context


class SessionDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = ('academics.delete_session', 'academics.delete_attendance')
    http_method_names = ('post',)
    model = Session
    success_url = reverse_lazy('teacher:attendance:list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        super().delete(request, *args, **kwargs)
        Attendance.objects.filter(session=self.object).delete()
        messages.success(request, 'Session deleted successfully')
        return redirect(self.get_success_url())

    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


class AttendanceSheetUpsertView(View):

    def get_object(self):
        cell = TimetableCell.objects.get(id=self.kwargs['pk'])
        if cell.subject_class.teacher.user != self.request.user:
            messages.info(self.request, "not allowed")
            return redirect(reverse("teacher:timetable"))
        return cell

    def get(self, request, *args, **kwargs):
        cell = self.get_object()
        with transaction.atomic():
            session, created = Session.objects.get_or_create(
                teacher=cell.subject_class.teacher,
                school_class=cell.school_class,
                subject=cell.subject_class.subject,
                period=cell.period_number,
                date=cell.timetable.created_at.date(),
            )

            if created:
                enrollments = Enrollment.objects.filter(school_class=session.school_class)
                for enrollment in enrollments:
                    Attendance.objects.create(
                        session=session,
                        student=enrollment.student,
                    )
        return redirect(reverse_lazy("teacher:attendance:detail", kwargs={'pk': session.pk}))


class MarkAttendance(View):

    def get_object(self):
        return Session.objects.get(pk=self.kwargs['pk'])

    def get_success_url(self):
        return reverse_lazy('teacher:timetable')

    def get_cell(self):
        session = self.get_object()
        cell = TimetableCell.objects.filter(
            school_class=session.school_class,
            subject_class__subject=session.subject,
            period_number=session.period,
            created_at__date=session.date
        )
        return cell

    def post(self, request, *args, **kwargs):
        with transaction.atomic():
            session = self.get_object()
            attendances = Attendance.objects.filter(session=session)

            for attendance in attendances:
                status_val = request.POST.get(f'attendance_{attendance.pk}')
                if status_val in ('1', '2', '3'):
                    attendance.status = int(status_val)
                    attendance.save()

            cell = self.get_cell()
            if cell:
                cell = cell.last()
                cell.is_marked = True
                cell.save()
        messages.success(request, "Attendance saved successfully!")
        return redirect(self.get_success_url())
