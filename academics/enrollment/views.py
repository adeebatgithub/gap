from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from controller.mixins import RedirectToDetail
from .forms import EnrollmentForm
from academics.models import Enrollment


class EnrollmentListView(ListView):
    model = Enrollment
    template_name = 'academics/enrollments/list.html'
    context_object_name = 'enrollments'

    def get_queryset(self):
        return Enrollment.objects.select_related(
            'student', 'school_class', 'academic_year'
        ).order_by('student__name')


class EnrollmentDetailView(DetailView):
    model = Enrollment
    template_name = 'academics/enrollments/detail.html'
    context_object_name = 'enrollment'

    def get_queryset(self):
        return Enrollment.objects.select_related('student', 'school_class', 'academic_year')


class EnrollmentCreateView(CreateView):
    model = Enrollment
    form_class = EnrollmentForm
    template_name = 'academics/enrollments/form.html'
    success_url = reverse_lazy('academics:enrollment:list')


class EnrollmentUpdateView(RedirectToDetail, UpdateView):
    model = Enrollment
    form_class = EnrollmentForm
    template_name = 'academics/enrollments/form.html'
    success_url = reverse_lazy('academics:enrollment:list')

    def get_detail_url(self):
        return reverse_lazy('academics:enrollment:detail', kwargs={'pk': self.object.pk})


class EnrollmentDeleteView(DeleteView):
    http_method_names = ('post',)
    model = Enrollment
    success_url = reverse_lazy('academics:enrollment:list')

    def get_detail_url(self):
        return reverse_lazy('academics:enrollment:detail', kwargs={'pk': self.object.pk})