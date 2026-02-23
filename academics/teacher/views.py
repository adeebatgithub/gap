from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from academics.models import Teacher, SubjectClass
from .forms import TeacherForm
from controller.mixins import RedirectToDetail

class TeacherListView(PermissionRequiredMixin, ListView):
    permission_required = "academics.view_teacher"
    model = Teacher
    template_name = 'academics/teachers/list.html'
    context_object_name = 'teachers'


class TeacherDetailView(PermissionRequiredMixin, DetailView):
    permission_required = "academics.view_teacher"
    model = Teacher
    template_name = 'academics/teachers/detail.html'
    context_object_name = 'teacher'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "assigned_subjects": SubjectClass.objects.filter(teacher=self.object),
        })
        return context


class TeacherCreateView(PermissionRequiredMixin, CreateView):
    permission_required = "academics.add_teacher"
    model = Teacher
    form_class = TeacherForm
    template_name = 'academics/teachers/form.html'
    success_url = reverse_lazy('academics:teacher:list')


class TeacherUpdateView(PermissionRequiredMixin, RedirectToDetail, UpdateView):
    permission_required = "academics.change_teacher"
    model = Teacher
    form_class = TeacherForm
    template_name = 'academics/teachers/form.html'
    success_url = reverse_lazy('academics:teacher:list')

    def get_detail_url(self):
        return reverse_lazy('academics:teacher:detail', kwargs={'pk': self.object.pk})


class TeacherDeleteView(PermissionRequiredMixin, RedirectToDetail, DeleteView):
    permission_required = "academics.delete_teacher"
    http_method_names = ['post']
    model = Teacher
    success_url = reverse_lazy('academics:teacher:list')

    def get_detail_url(self):
        reverse_lazy('academics:teacher:detail', kwargs={'pk': self.object.pk})