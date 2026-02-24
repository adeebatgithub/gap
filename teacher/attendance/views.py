from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db import transaction
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View

from .forms import SessionForm, SessionUpdateForm
from academics.models import Session, SchoolClass, Enrollment, Attendance, Teacher


class SessionListView(PermissionRequiredMixin, ListView):
    permission_required = 'academics.view_session'
    model = Session
    template_name = 'teacher/sessions/list.html'
    context_object_name = 'sessions'

    def get_queryset(self):
        return Session.objects.filter(teacher__user=self.request.user).order_by('-date', '-id')


class SessionDetailView(PermissionRequiredMixin, DetailView):
    permission_required = 'academics.view_session'
    model = Session
    template_name = 'teacher/sessions/detail.html'
    context_object_name = 'session'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "attendances": Attendance.objects.filter(session=self.object),
        })
        return context


class SessionCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'academics.add_session'
    model = Session
    form_class = SessionForm
    template_name = 'teacher/sessions/form.html'
    success_url = reverse_lazy('teacher:attendance:list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.teacher = Teacher.objects.get(user=self.request.user)
        with transaction.atomic():
            self.object = form.save()
            enrollments = Enrollment.objects.filter(school_class=self.object.school_class)
            for enrollment in enrollments:
                Attendance.objects.create(
                    session=self.object,
                    student=enrollment.student,
                )
        return redirect(self.get_success_url())


class SessionUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'academics.change_session'
    model = Session
    form_class = SessionUpdateForm
    template_name = 'teacher/sessions/form.html'
    success_url = reverse_lazy('teacher:attendance:list')


class SessionDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = 'academics.delete_session'
    http_method_names = ('post', )
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


class MarkAttendance(View):
    def get_object(self):
        return Session.objects.get(pk=self.kwargs['pk'])

    def get_success_url(self):
        return reverse_lazy('teacher:attendance:list')

    def post(self, request, *args, **kwargs):
        with transaction.atomic():
            session = self.get_object()
            attendances = Attendance.objects.filter(session=session)

            for attendance in attendances:
                status_val = request.POST.get(f'attendance_{attendance.pk}')
                if status_val in ('1', '2'):
                    attendance.status = int(status_val)
                    attendance.save()
        messages.success(request, "Attendance saved successfully!")
        return redirect(self.get_success_url())
