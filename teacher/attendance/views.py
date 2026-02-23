from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db import transaction
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import SessionForm, SessionUpdateForm
from academics.models import Session, SchoolClass, Enrollment, Attendance


class SessionListView(PermissionRequiredMixin, ListView):
    permission_required = 'academics.view_session'
    model = Session
    template_name = 'teacher/sessions/list.html'
    context_object_name = 'sessions'

    def get_queryset(self):
        return Session.objects.filter(teacher__user=self.request.user).order_by('-date')


class SessionDetailView(PermissionRequiredMixin, DetailView):
    permission_required = 'academics.view_session'
    model = Session
    template_name = 'teacher/sessions/detail.html'
    context_object_name = 'session'

    def get_context_data(self, **kwargs):
        Session.objects.all().prefetch_related('attendance_set')


class SessionCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'academics.add_session'
    model = Session
    form_class = SessionForm
    template_name = 'teacher/sessions/form.html'
    success_url = reverse_lazy('teacher:attendance:list')

    def form_valid(self, form):
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
