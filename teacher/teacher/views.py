from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from academics.subject.models import SubjectClass
from controller.mixins import RedirectToDetail
from teacher.teacher.models import Teacher
from .forms import TeacherForm


class TeacherListView(PermissionRequiredMixin, ListView):
    permission_required = "teacher.view_teacher"
    model = Teacher
    template_name = 'teacher/teachers/list.html'
    context_object_name = 'teachers'

    def get_template_names(self):
        if self.request.htmx:
            return ['teacher/teachers/partial_list.html']
        return super().get_template_names()

    def get_queryset(self):
        search = self.request.GET.get("search", "")
        queryset = super().get_queryset()
        if search:
            queryset = queryset.filter(
                Q(user__first_name__icontains=search) |
                Q(user__last_name__icontains=search)
            )

        return queryset.order_by("user__first_name", "user__last_name")


class TeacherDetailView(PermissionRequiredMixin, DetailView):
    permission_required = "teacher.view_teacher"
    model = Teacher
    template_name = 'teacher/teachers/detail.html'
    context_object_name = 'teacher'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "assigned_subjects": SubjectClass.objects.filter(teacher=self.object),
        })
        return context


class TeacherCreateView(PermissionRequiredMixin, CreateView):
    permission_required = "teacher.add_teacher"
    model = Teacher
    form_class = TeacherForm
    template_name = 'teacher/teachers/form.html'
    success_url = reverse_lazy('academics:teacher:list')


class TeacherUpdateView(PermissionRequiredMixin, RedirectToDetail, UpdateView):
    permission_required = "teacher.change_teacher"
    model = Teacher
    form_class = TeacherForm
    template_name = 'teacher/teachers/form.html'
    success_url = reverse_lazy('academics:teacher:list')

    def get_detail_url(self):
        return reverse_lazy('academics:teacher:detail', kwargs={'pk': self.object.pk})


class TeacherDeleteView(PermissionRequiredMixin, RedirectToDetail, DeleteView):
    permission_required = "teacher.delete_teacher"
    http_method_names = ['post']
    model = Teacher
    success_url = reverse_lazy('academics:teacher:list')

    def get_detail_url(self):
        reverse_lazy('academics:teacher:detail', kwargs={'pk': self.object.pk})


class AddToGroup(PermissionRequiredMixin, DetailView):
    permission_required = "teacher.change_teacher"
    model = Teacher
    group = None

    def get_group(self):
        return self.group

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        user = self.object.user
        user.groups.add(self.get_group())
        user.save()
        return redirect(reverse_lazy('teacher:teacher:list'))


class RemoveFromGroup(PermissionRequiredMixin, DetailView):
    permission_required = "teacher.change_teacher"
    model = Teacher
    group = None

    def get_group(self):
        return self.group

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        user = self.object.user
        user.groups.remove(self.get_group())
        user.save()
        return redirect(reverse_lazy('teacher:teacher:list'))


class AddToAdmin(AddToGroup):
    def get_group(self):
        return Group.objects.get(name="Admin")


class AddToExam(AddToGroup):
    def get_group(self):
        return Group.objects.get(name="Exam")


class RemoveFromAdmin(RemoveFromGroup):
    def get_group(self):
        return Group.objects.get(name="Admin")


class RemoveFromExam(RemoveFromGroup):
    def get_group(self):
        return Group.objects.get(name="Exam")
