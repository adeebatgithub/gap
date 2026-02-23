from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import SubjectForm
from academics.models import Subject


class SubjectListView(PermissionRequiredMixin, ListView):
    permission_required = "academics.view_subject"
    model = Subject
    template_name = 'academics/subjects/list.html'
    context_object_name = 'subjects'


class SubjectDetailView(PermissionRequiredMixin, DetailView):
    permission_required = "academics.view_subject"
    model = Subject
    template_name = 'academics/subjects/detail.html'
    context_object_name = 'subject'


class SubjectCreateView(PermissionRequiredMixin, CreateView):
    permission_required = "academics.add_subject"
    model = Subject
    form_class = SubjectForm
    template_name = 'academics/subjects/form.html'
    success_url = reverse_lazy('academics:subject:list')


class SubjectUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = "academics.change_subject"
    model = Subject
    form_class = SubjectForm
    template_name = 'academics/subjects/form.html'
    success_url = reverse_lazy('academics:subject:list')


class SubjectDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = "academics.delete_subject"
    http_method_names = ("post",)
    model = Subject
    success_url = reverse_lazy('academics:subject:list')
