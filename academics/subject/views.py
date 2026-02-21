from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import SubjectForm
from academics.models import Subject


class SubjectListView(ListView):
    model = Subject
    template_name = 'academics/subjects/list.html'
    context_object_name = 'subjects'


class SubjectDetailView(DetailView):
    model = Subject
    template_name = 'academics/subjects/detail.html'
    context_object_name = 'subject'


class SubjectCreateView(CreateView):
    model = Subject
    form_class = SubjectForm
    template_name = 'academics/subjects/form.html'
    success_url = reverse_lazy('academics:subject:list')


class SubjectUpdateView(UpdateView):
    model = Subject
    form_class = SubjectForm
    template_name = 'academics/subjects/form.html'
    success_url = reverse_lazy('academics:subject:list')


class SubjectDeleteView(DeleteView):
    http_method_names = ("post",)
    model = Subject
    success_url = reverse_lazy('academics:subject:list')
