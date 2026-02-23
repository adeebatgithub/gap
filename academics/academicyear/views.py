from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin

from .forms import AcademicYearForm
from academics.models import AcademicYear


class AcademicYearListView(PermissionRequiredMixin, ListView):
    permission_required = "academics.view_academicyear"
    model = AcademicYear
    template_name = 'academics/year/list.html'
    context_object_name = 'academic_years'


class AcademicYearCreateView(PermissionRequiredMixin, CreateView):
    permission_required = "academics.add_academicyear"
    model = AcademicYear
    form_class = AcademicYearForm
    template_name = 'academics/year/form.html'
    success_url = reverse_lazy('academics:academicyear:list')

    def get_success_url(self):
        self.request.session["is_academic_year_set"] = 1
        return super().get_success_url()


class AcademicYearUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = "academics.change_academicyear"
    model = AcademicYear
    form_class = AcademicYearForm
    template_name = 'academics/year/form.html'
    success_url = reverse_lazy('academics:academicyear:list')


class AcademicYearDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = "academics.delete_academicyear"
    http_method_names = ("post",)
    model = AcademicYear
    success_url = reverse_lazy('academics:academicyear:list')
