from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import AcademicYearForm
from academics.models import AcademicYear


class AcademicYearListView(ListView):
    model = AcademicYear
    template_name = 'academics/year/list.html'
    context_object_name = 'academic_years'
    paginate_by = 10
    ordering = ['-start_date']


class AcademicYearCreateView(CreateView):
    model = AcademicYear
    form_class = AcademicYearForm
    template_name = 'academics/year/form.html'
    success_url = reverse_lazy('academics:academicyear:list')


class AcademicYearUpdateView(UpdateView):
    model = AcademicYear
    form_class = AcademicYearForm
    template_name = 'academics/year/form.html'
    success_url = reverse_lazy('academics:academicyear:list')


class AcademicYearDeleteView(DeleteView):
    http_method_names = ("post",)
    model = AcademicYear
    success_url = reverse_lazy('academics:academicyear:list')
