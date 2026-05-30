from django.http.response import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, DeleteView

from controller.views import ExportAsXlsxView
from .forms import AdmissionForm
from .models import Admission


class AdmissionListView(ListView):
    model = Admission
    context_object_name = "admissions"
    template_name = "academics/admission/list.html"

    def get_template_names(self):
        if self.request.htmx:
            return ["academics/admission/partial_list.html"]
        return super().get_template_names()

    def get_filters(self):
        filters = {}
        if self.request.GET.get("date_from"):
            filters["created_at__gte"] = self.request.GET.get("date_from")

        if self.request.GET.get("date_to"):
            filters["created_at__lte"] = self.request.GET.get("date_to")

        if self.request.GET.get("search"):
            filters["full_name__icontains"] = self.request.GET.get("search")

        return filters

    def get_queryset(self):
        return Admission.objects.filter(**self.get_filters())


class AdmissionDetailView(DetailView):
    model = Admission
    template_name = "academics/admission/detail.html"


class AdmissionCreateView(CreateView):
    model = Admission
    form_class = AdmissionForm
    http_method_names = ["post"]
    template_name = "front/partials/application_form.html"

    def form_valid(self, form):
        self.object = form.save()

        response = HttpResponse(status=200)
        response["HX-TRIGGER"] = "SubmitSuccess"
        return response


class AdmissionUpdateView(UpdateView):
    model = Admission
    form_class = AdmissionForm
    template_name = "academics/admission/form.html"
    success_url = reverse_lazy("academics:admission:list")


class AdmissionDeleteView(DeleteView):
    model = Admission
    success_url = reverse_lazy("academics:admission:list")

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().delete(request, *args, **kwargs)


class AdmissionExportView(ExportAsXlsxView):
    workbook_title = "admissions"
    filename = "admissions.xlsx"
    model = Admission
    fields = [
        "full_name",
        "guardian_name",
        "dob",
        "mother_tongue",
        "course",
        "house_name",
        "pincode",
        "post",
        "district",
        "state",
        "phone_1",
        "phone_2",
        "center",
    ]

    def get_filters(self):
        filters = {}
        if self.request.GET.get("date_from"):
            filters["created_at__gte"] = self.request.GET.get("date_from")

        if self.request.GET.get("date_to"):
            filters["created_at__lte"] = self.request.GET.get("date_to")

        return filters
