from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db import transaction
from django.db.models import Count, F
from django.http.response import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import DetailView, DeleteView, View, TemplateView, ListView, CreateView, UpdateView
from openpyxl.workbook.workbook import Workbook

from academics.enrollment.models import Enrollment
from academics.schoolclass.models import SchoolClass
from academics.subject.models import SubjectClass
from controller.utils import get_academic_year
from teacher.attendance.models import Session, Attendance
from teacher.teacher.models import Teacher
from timetable.models import TimetableCell
from .forms import SessionForm, SessionUpdateForm
from .utils import get_leafnodes


class SessionListView(PermissionRequiredMixin, ListView):
    permission_required = 'teacher.view_session'
    model = Session
    template_name = 'teacher/sessions/list.html'
    context_object_name = 'sessions'

    def get_template_names(self):
        if self.request.htmx:
            return ["teacher/sessions/partial_list.html"]
        return super().get_template_names()

    def get_filters(self):
        filters = {}
        if self.request.GET.get('date'):
            filters['date'] = self.request.GET.get('date')
        else:
            filters['date'] = timezone.localdate()

        if self.request.GET.get('class'):
            filters['subject_class__school_class_id'] = self.request.GET.get('class')

        return filters

    def get_queryset(self):
        return (
                Session.objects.select_related(
                "subject_class__teacher__user",
                "subject_class__school_class",
                "subject_class__subject",
            )
            .filter(subject_class__teacher__user=self.request.user, **self.get_filters())
            .order_by('-date', '-id')
        )


class SessionDetailView(PermissionRequiredMixin, DetailView):
    permission_required = ('teacher.view_session', 'teacher.view_attendance')
    model = Session
    template_name = 'teacher/sessions/detail.html'
    context_object_name = 'session'

    def get_queryset(self):
        return super().get_queryset().select_related(
            "subject_class__school_class",
            "subject_class__teacher",
            "subject_class__teacher__user",
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(get_leafnodes(self.object.subject_class.school_class))
        context.update({
            "attendances": Attendance.objects.select_related("student").filter(session=self.object).order_by("student__name"),
        })
        return context


class SessionCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'teacher.add_session'
    model = Session
    form_class = SessionForm
    template_name = 'teacher/sessions/form.html'

    def get_success_url(self):
        return reverse_lazy("teacher:attendance:detail", kwargs={"pk": self.object.pk})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_initial(self):
        return {
            "date": timezone.localdate(),
        }

    def form_valid(self, form):
        form.instance.teacher = Teacher.objects.get(user=self.request.user)
        with transaction.atomic():
            self.object = form.save()
            enrollments = Enrollment.objects.filter(school_class__in=get_leafnodes(self.object.subject_class.school_class))
            for enrollment in enrollments:
                Attendance.objects.create(
                    session=self.object,
                    student=enrollment.student,
                )
        return redirect(self.get_success_url())


class SessionUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'teacher.change_session'
    model = Session
    form_class = SessionUpdateForm
    template_name = 'teacher/sessions/form.html'
    success_url = reverse_lazy('teacher:attendance:list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class SessionDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = ('teacher.delete_session', 'teacher.delete_attendance')
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
        if self.request.user.is_member("Admin"):
            return cell

        if cell.subject_class.teacher.user != self.request.user:
            return None
        return cell

    def get(self, request, *args, **kwargs):
        cell = self.get_object()
        if cell is None:
            messages.info(self.request, "not allowed")
            return redirect(reverse_lazy("teacher:timetable"))

        with transaction.atomic():
            session, created = Session.objects.get_or_create(
                subject_class=cell.subject_class,
                period=cell.period_number,
                date=cell.timetable.created_at.date(),
            )

            if created:
                enrollments = Enrollment.objects.filter(school_class=session.subject_class.school_class)
                for enrollment in enrollments:
                    Attendance.objects.create(
                        session=session,
                        student=enrollment.student,
                    )
        return redirect(reverse_lazy("teacher:attendance:detail", kwargs={'pk': session.pk}))


class MarkAttendance(View):

    def get_object(self):
        session = Session.objects.get(pk=self.kwargs['pk'])
        if session.created_at.date() != timezone.localdate():
            return None
        return session

    def get_success_url(self):
        return reverse_lazy("teacher:attendance:list")

    def get_cell(self):
        session = self.get_object()
        cell = TimetableCell.objects.filter(
            school_class=session.subject_class.school_class,
            subject_class=session.subject_class,
            period_number=session.period,
        )
        return cell

    def post(self, request, *args, **kwargs):
        with transaction.atomic():
            session = self.get_object()
            if session is None:
                messages.info(self.request, "not allowed")
                return redirect(reverse_lazy("teacher:attendance:list"))

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


class AttendanceReportView(PermissionRequiredMixin, TemplateView):
    permission_required = ('teacher.view_session', 'teacher.view_attendance')
    template_name = 'teacher/report/attendance.html'

    def get_template_names(self):
        if self.request.htmx:
            return ["teacher/report/partials/attendance.html"]
        return super().get_template_names()

    def get_queryset(self):
        filters = {
            "session__subject_class__school_class__academic_year__id": get_academic_year(self.request),
        }
        if self.request.GET.get('class_name'):
            filters["session__subject_class__school_class__name"] = self.request.GET.get('class_name')
        return Attendance.objects.filter(**filters)

    def get_session_lookup(self):
        session_totals = (
            Session.objects
            .annotate(
                class_name=F("subject_class__school_class__name"),
                teacher_code=F("subject_class__teacher__code"),
                subject_name=F("subject_class__subject__name"),
            )
            .values(
                "class_name",
                "teacher_code",
                "subject_name",
            )
            .annotate(total=Count("id"))
        )
        session_lookup = {
            (
                row["class_name"],
                row["teacher_code"],
                row["subject_name"],
            ): row["total"]
            for row in session_totals
        }
        return session_lookup

    def get_report(self):
        queryset = (
            self.get_queryset()
            .annotate(
                class_name=F("session__subject_class__school_class__name"),
                teacher_code=F("session__subject_class__teacher__code"),
                subject_name=F("session__subject_class__subject__name"),
                student_name=F("student__name"),
            )
            .values("class_name", "teacher_code", "subject_name", "student_name")
            .filter(status=Attendance.PRESENT)
            .annotate(present_count=Count("id"))
        )

        data = {}
        session_lookup = self.get_session_lookup()
        for row in queryset:
            class_name = row["class_name"]
            subject_name = row["subject_name"]
            teacher_code = row["teacher_code"]
            subject_full = f"{subject_name} ({teacher_code})"
            student_name = row["student_name"]
            present_count = row["present_count"]

            if class_name not in data:
                data[class_name] = {
                    "subjects": {"zTotal", "zz%"},
                    "students": {"out of": {"zTotal": 0, "zz%": "100"}}
                }

            data[class_name]["subjects"].add(subject_full)
            if student_name not in data[class_name]["students"]:
                data[class_name]["students"][student_name] = {}
                data[class_name]["students"][student_name]["zTotal"] = 0
                data[class_name]["students"][student_name]["zz%"] = 0

            data[class_name]["students"][student_name][subject_full] = present_count
            data[class_name]["students"][student_name]["zTotal"] += present_count

            session_total = session_lookup.get(
                (class_name, teacher_code, subject_name),
                0
            )
            if subject_full not in data[class_name]["students"]["out of"]:
                data[class_name]["students"]["out of"][subject_full] = session_total
                data[class_name]["students"]["out of"]["zTotal"] += session_total

            if data[class_name]["students"]["out of"]["zTotal"] > 0:
                data[class_name]["students"][student_name]["zz%"] = round(
                    (data[class_name]["students"][student_name]["zTotal"] / data[class_name]["students"]["out of"]["zTotal"]) * 100
                )

        for class_data in data.values():
            class_data["subjects"] = sorted(class_data["subjects"])

        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "report": self.get_report(),
            "classes": SchoolClass.objects.only("name"),
        })
        return context


class AttendanceExportView(AttendanceReportView):
    permission_required = ('teacher.view_session', 'teacher.view_attendance')

    @staticmethod
    def remove_z(header):
        if header[0] == "z":
            return header.replace("z", "")
        return header

    def get(self, request, *args, **kwargs):
        workbook = Workbook()
        report = self.get_report()
        for class_name, data in report.items():
            worksheet = workbook.create_sheet(class_name)
            subjects = ["Student Name"] + data["subjects"]
            worksheet.append([self.remove_z(x) for x in subjects])
            for student_name, present_count in data["students"].items():
                worksheet.append([student_name] + [present_count.get(x) for x in data["subjects"]])

        response = HttpResponse(
            content_type=(
                "application/vnd.openxmlformats-officedocument."
                "spreadsheetml.sheet"
            )
        )
        response["Content-Disposition"] = (
            f'attachment; filename="attendance_{timezone.localdate().year}.xlsx"'
        )
        workbook.save(response)
        return response
