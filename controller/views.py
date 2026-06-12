from django.conf import settings
from django.db.models import F, Count
from django.http.response import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.base import View
from openpyxl.workbook.workbook import Workbook

from academics.schoolclass.models import SchoolClass
from teacher.attendance.models import Attendance, Session
from controller.utils import get_academic_year


class MaintenanceView(TemplateView):
    template_name = "controller/maintenance.html"

    def get(self, request, *args, **kwargs):
        if not getattr(settings, "MAINTENANCE_MODE", False):
            return redirect(reverse_lazy("users:redirect-user"))
        return super().get(request, *args, **kwargs)


class UnderConstructionView(TemplateView):
    template_name = "controller/underdev.html"


class TestView(TemplateView):
    template_name = 'teacher/report/attendance.html'

    def get_template_names(self):
        if self.request.htmx:
            return ["teacher/report/partials/attendance.html"]
        return super().get_template_names()

    def get_queryset(self):
        filters = {
            "session__subject_class__school_class__academic_year__id": get_academic_year(self.request),
        }
        if self.request.GET.get('class_name'):
            filters["session__subject_class__school_class__name"] = self.request.GET.get('class_name')
        return Attendance.objects.filter(**filters)

    def get_session_lookup(self):
        session_totals = (
            Session.objects
            .annotate(
                class_name=F("subject_class__school_class__name"),
                teacher_code=F("subject_class__teacher__code"),
                subject_name=F("subject_class__subject__name"),
            )
            .values(
                "class_name",
                "teacher_code",
                "subject_name",
            )
            .annotate(total=Count("id"))
        )
        session_lookup = {
            (
                row["class_name"],
                row["teacher_code"],
                row["subject_name"],
            ): row["total"]
            for row in session_totals
        }
        return session_lookup

    def get_report(self):
        queryset = (
            self.get_queryset()
            .annotate(
                class_name=F("session__subject_class__school_class__name"),
                teacher_code=F("session__subject_class__teacher__code"),
                subject_name=F("session__subject_class__subject__name"),
                student_name=F("student__name"),
            )
            .values("class_name", "teacher_code", "subject_name", "student_name")
            .filter(status=Attendance.PRESENT)
            .annotate(present_count=Count("id"))
        )

        data = {}
        session_lookup = self.get_session_lookup()
        for row in queryset:
            class_name = row["class_name"]
            subject_name = row["subject_name"]
            teacher_code = row["teacher_code"]
            subject_full = f"{subject_name} ({teacher_code})"
            student_name = row["student_name"]
            present_count = row["present_count"]

            if class_name not in data:
                data[class_name] = {
                    "subjects": {"zTotal", "zz%"},
                    "students": {"out of": {"zTotal": 0, "zz%": "100"}}
                }

            data[class_name]["subjects"].add(subject_full)
            if student_name not in data[class_name]["students"]:
                data[class_name]["students"][student_name] = {}
                data[class_name]["students"][student_name]["zTotal"] = 0
                data[class_name]["students"][student_name]["zz%"] = 0

            data[class_name]["students"][student_name][subject_full] = present_count
            data[class_name]["students"][student_name]["zTotal"] += present_count

            session_total = session_lookup.get(
                (class_name, teacher_code, subject_name),
                0
            )
            if subject_full not in data[class_name]["students"]["out of"]:
                data[class_name]["students"]["out of"][subject_full] = session_total
                data[class_name]["students"]["out of"]["zTotal"] += session_total

            if data[class_name]["students"]["out of"]["zTotal"] > 0:
                data[class_name]["students"][student_name]["zz%"] = round(
                    (data[class_name]["students"][student_name]["zTotal"] / data[class_name]["students"]["out of"]["zTotal"]) * 100
                )

        for class_data in data.values():
            class_data["subjects"] = sorted(class_data["subjects"])

        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "report": self.get_report(),
            "classes": SchoolClass.objects.only("name"),
        })
        return context


class ExportAsXlsxView(View):
    workbook_title = "Export"
    filename = "export.xlsx"

    model = None
    fields = []
    headers = None

    def get_filters(self) -> dict:
        return {}

    def get_queryset(self):
        return self.model.objects.filter(**self.get_filters())

    def get_headers(self):
        """
        Return excel column headers.
        """
        return self.headers or self.fields

    def get_row(self, obj):
        """
        Return row values for a model instance.
        """
        row = []

        for field in self.fields:
            value = getattr(obj, field)
            if callable(value):
                value = value()

            row.append(str(value))
        return row

    def get_sheet(self):
        workbook = Workbook()
        worksheet = workbook.active
        worksheet.title = self.workbook_title
        worksheet.append(self.get_headers())

        queryset = self.get_queryset()
        for obj in queryset.iterator():
            worksheet.append(self.get_row(obj))
        return workbook

    def get(self, request, *args, **kwargs):
        if not self.model:
            raise ValueError("model is required")

        if not self.fields:
            raise ValueError("fields cannot be empty")

        response = HttpResponse(
            content_type=(
                "application/vnd.openxmlformats-officedocument."
                "spreadsheetml.sheet"
            )
        )
        response["Content-Disposition"] = (
            f'attachment; filename="{self.filename}"'
        )
        workbook = self.get_sheet()
        workbook.save(response)
        return response
