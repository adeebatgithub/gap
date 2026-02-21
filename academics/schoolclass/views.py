from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from controller.mixins import RedirectToDetail
from .forms import SchoolClassForm
from academics.models import SchoolClass


class SchoolClassListView(ListView):
    model = SchoolClass
    template_name = 'academics/schoolclass/list.html'
    context_object_name = 'classes'


class SchoolClassDetailView(DetailView):
    model = SchoolClass
    template_name = 'academics/schoolclass/detail.html'
    context_object_name = 'school_class'


class SchoolClassCreateView(CreateView):
    model = SchoolClass
    form_class = SchoolClassForm
    template_name = 'academics/schoolclass/form.html'
    success_url = reverse_lazy('academics:schoolclass:list')


class SchoolClassUpdateView(RedirectToDetail, UpdateView):
    model = SchoolClass
    form_class = SchoolClassForm
    template_name = 'academics/schoolclass/form.html'
    success_url = reverse_lazy('academics:schoolclass:list')

    def get_detail_url(self):
        return reverse_lazy('academics:schoolclass:detail', kwargs={'pk': self.object.pk})


class SchoolClassDeleteView(RedirectToDetail, DeleteView):
    http_method_names = ("post",)
    model = SchoolClass
    success_url = reverse_lazy('academics:schoolclass:list')

    def get_detail_url(self):
        return reverse_lazy('academics:schoolclass:detail', kwargs={'pk': self.object.pk})
