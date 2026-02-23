from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from controller.mixins import RedirectToDetail
from .forms import SchoolClassForm
from academics.models import SchoolClass, SubjectClass, Enrollment


class SchoolClassListView(PermissionRequiredMixin, ListView):
    permission_required = "academics.view_schoolclass"
    model = SchoolClass
    template_name = 'academics/schoolclass/list.html'
    context_object_name = 'classes'


class SchoolClassDetailView(PermissionRequiredMixin, DetailView):
    permission_required = "academics.view_schoolclass"
    model = SchoolClass
    template_name = 'academics/schoolclass/detail.html'
    context_object_name = 'school_class'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "assigned_teachers": SubjectClass.objects.filter(school_class=self.object),
            "enrollments": Enrollment.objects.filter(school_class=self.object),
        })
        return context


class SchoolClassCreateView(PermissionRequiredMixin, CreateView):
    permission_required = "academics.add_schoolclass"
    model = SchoolClass
    form_class = SchoolClassForm
    template_name = 'academics/schoolclass/form.html'
    success_url = reverse_lazy('academics:schoolclass:list')


class SchoolClassUpdateView(PermissionRequiredMixin, RedirectToDetail, UpdateView):
    permission_required = "academics.change_schoolclass"
    model = SchoolClass
    form_class = SchoolClassForm
    template_name = 'academics/schoolclass/form.html'
    success_url = reverse_lazy('academics:schoolclass:list')

    def get_detail_url(self):
        return reverse_lazy('academics:schoolclass:detail', kwargs={'pk': self.object.pk})


class SchoolClassDeleteView(PermissionRequiredMixin, RedirectToDetail, DeleteView):
    permission_required = "academics.delete_schoolclass"
    http_method_names = ("post",)
    model = SchoolClass
    success_url = reverse_lazy('academics:schoolclass:list')

    def get_detail_url(self):
        return reverse_lazy('academics:schoolclass:detail', kwargs={'pk': self.object.pk})
