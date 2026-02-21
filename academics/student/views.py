from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import StudentForm
from academics.models import Student


class StudentListView(ListView):
    model = Student
    template_name = 'academics/students/list.html'
    context_object_name = 'students'
    paginate_by = 10


class StudentDetailView(DetailView):
    model = Student
    template_name = 'academics/students/detail.html'
    context_object_name = 'student'


class StudentCreateView(CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'academics/students/form.html'
    success_url = reverse_lazy('academics:student:list')


class StudentUpdateView(UpdateView):
    model = Student
    form_class = StudentForm
    template_name = 'academics/students/form.html'
    success_url = reverse_lazy('academics:student:list')


class StudentDeleteView(DeleteView):
    http_method_names = ("post",)
    model = Student
    success_url = reverse_lazy('academics:student:list')
