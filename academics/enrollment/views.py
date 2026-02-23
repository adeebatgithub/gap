from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from controller.mixins import RedirectToDetail
from .forms import EnrollmentForm
from academics.models import Enrollment, SchoolClass, Attendance


class EnrollmentListView(PermissionRequiredMixin, ListView):
    permission_required = "academics.view_enrollment"
    model = Enrollment
    template_name = 'academics/enrollments/list.html'
    context_object_name = 'enrollments'

    def get_queryset(self):
        return Enrollment.objects.select_related(
            'student', 'school_class', 'academic_year'
        ).order_by('student__name')


class EnrollmentDetailView(PermissionRequiredMixin, DetailView):
    permission_required = "academics.view_enrollment"
    model = Enrollment
    template_name = 'academics/enrollments/detail.html'
    context_object_name = 'enrollment'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "attendances": Attendance.objects.filter(student=self.object.student, session__date=timezone.localdate())
        })
        return context


class EnrollmentCreateView(PermissionRequiredMixin, CreateView):
    permission_required = "academics.add_enrollment"
    model = Enrollment
    form_class = EnrollmentForm
    template_name = 'academics/enrollments/form.html'
    success_url = reverse_lazy('academics:enrollment:list')

    def get_initial(self):
        initial = super().get_initial()
        if self.request.GET.get('schoolclass'):
            initial.update({
                "school_class": SchoolClass.objects.get(id=self.request.GET.get('schoolclass')),
            })
        return initial

    def get_success_url(self):
        if self.request.GET.get('schoolclass'):
            return reverse_lazy('academics:schoolclass:detail', kwargs={'pk': self.request.GET.get('schoolclass')})
        return super().get_success_url()


class EnrollmentUpdateView(PermissionRequiredMixin, RedirectToDetail, UpdateView):
    permission_required = "academics.change_enrollment"
    model = Enrollment
    form_class = EnrollmentForm
    template_name = 'academics/enrollments/form.html'
    success_url = reverse_lazy('academics:enrollment:list')

    def get_detail_url(self):
        return reverse_lazy('academics:enrollment:detail', kwargs={'pk': self.object.pk})

    def get_success_url(self):
        if self.request.GET.get('schoolclass'):
            return reverse_lazy('academics:schoolclass:detail', kwargs={'pk': self.request.GET.get('schoolclass')})
        return super().get_success_url()


class EnrollmentDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = "academics.delete_enrollment"
    http_method_names = ('post',)
    model = Enrollment
    success_url = reverse_lazy('academics:enrollment:list')

    def get_detail_url(self):
        return reverse_lazy('academics:enrollment:detail', kwargs={'pk': self.object.pk})

    def get_success_url(self):
        if self.request.GET.get('schoolclass'):
            return reverse_lazy('academics:schoolclass:detail', kwargs={'pk': self.request.GET.get('schoolclass')})
        return super().get_success_url()