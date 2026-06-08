from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.base import RedirectView
from django.views.generic.detail import SingleObjectMixin

from controller.mixins import RedirectToDetail
from controller.utils import get_academic_year
from .forms import SchoolClassForm
from academics.schoolclass.models import SchoolClass
from academics.subject.models import SubjectClass
from academics.enrollment.models import Enrollment


class SchoolClassListView(PermissionRequiredMixin, ListView):
    permission_required = "academics.view_schoolclass"
    model = SchoolClass
    template_name = 'academics/schoolclass/list.html'
    context_object_name = 'classes'

    def get_template_names(self):
        if self.request.htmx:
            return ['academics/schoolclass/partial_list.html']
        return super().get_template_names()

    def get_filters(self):
        filters = {
            "academic_year__id": get_academic_year(self.request)
        }
        if search := self.request.GET.get('search'):
            filters['name__icontains'] = search
        return filters

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(**self.get_filters())


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

    def form_valid(self, form):
        form.instance.academic_year_id = get_academic_year(self.request)
        return super().form_valid(form)


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
