from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from academics.models import Teacher
from .forms import TeacherForm
from controller.mixins import RedirectToDetail

class TeacherListView(ListView):
    model = Teacher
    template_name = 'academics/teachers/list.html'
    context_object_name = 'teachers'


class TeacherDetailView(DetailView):
    model = Teacher
    template_name = 'academics/teachers/detail.html'
    context_object_name = 'teacher'


class TeacherCreateView(CreateView):
    model = Teacher
    form_class = TeacherForm
    template_name = 'academics/teachers/form.html'
    success_url = reverse_lazy('academics:teacher:list')


class TeacherUpdateView(RedirectToDetail, UpdateView):
    model = Teacher
    form_class = TeacherForm
    template_name = 'academics/teachers/form.html'
    success_url = reverse_lazy('academics:teacher:list')

    def get_detail_url(self):
        return reverse_lazy('academics:teacher:detail', kwargs={'pk': self.object.pk})


class TeacherDeleteView(RedirectToDetail, DeleteView):
    http_method_names = ['post']
    model = Teacher
    success_url = reverse_lazy('academics:teacher:list')

    def get_detail_url(self):
        reverse_lazy('academics:teacher:detail', kwargs={'pk': self.object.pk})