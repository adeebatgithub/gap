from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView

from academics.models import SubjectClass, Teacher, SchoolClass
from .forms import SubjectClassForm
from .mixin import RedirectToFrom


class SubjectClassCreateView(PermissionRequiredMixin, RedirectToFrom, CreateView):
    permission_required = "academics.add_subjectclass"
    model = SubjectClass
    form_class = SubjectClassForm
    template_name = 'academics/assignment/form.html'

    def get_initial(self):
        if self.request.GET.get("teacher"):
            return {
                'teacher': Teacher.objects.get(id=self.request.GET.get("teacher"))
            }
        elif self.request.GET.get("schoolclass"):
            return {
                "school_class": SchoolClass.objects.get(id=self.request.GET.get("schoolclass"))
            }
        return {}


class SubjectClassUpdateView(PermissionRequiredMixin, RedirectToFrom, UpdateView):
    permission_required = "academics.change_subjectclass"
    model = SubjectClass
    form_class = SubjectClassForm
    template_name = 'academics/assignment/form.html'


class SubjectClassDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = "academics.delete_subjectclass"
    http_method_names = ("post",)
    model = SubjectClass

    def get_success_url(self):
        if self.request.POST.get("teacher"):
            return reverse_lazy("academics:teacher:detail", kwargs={"pk": self.request.POST.get("teacher")})

        elif self.request.POST.get("schoolclass"):
            return reverse_lazy("academics:schoolclass:detail", kwargs={"pk": self.request.POST.get("schoolclass")})

        return reverse_lazy("academics:dashboard")
