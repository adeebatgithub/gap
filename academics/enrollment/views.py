from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.cache import cache
from django.db import transaction
from django.db.models.aggregates import Count
from django.db.models.expressions import F
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.base import RedirectView
from django.views.generic.detail import SingleObjectMixin

from academics.enrollment.models import Student, Enrollment
from academics.schoolclass.models import SchoolClass
from controller.mixins import RedirectToDetail
from controller.utils import get_academic_year
from teacher.attendance.models import Attendance, Session
from .forms import EnrollmentForm


class EnrollmentListView(PermissionRequiredMixin, ListView):
    permission_required = "academics.view_enrollment"
    model = Enrollment
    template_name = 'academics/enrollments/list.html'
    context_object_name = 'enrollments'

    def get_template_names(self):
        if self.request.htmx:
            return ['academics/enrollments/partial_list.html']
        return super().get_template_names()

    def get_filters(self):
        filters = {"school_class__academic_year__id": get_academic_year(self.request)}
        if search := self.request.GET.get('search'):
            filters['student__name__icontains'] = search

        if class_name := self.request.GET.get('class_name'):
            filters['school_class__name__icontains'] = class_name

        return filters

    def get_queryset(self):
        queryset = Enrollment.objects.filter(**self.get_filters()).select_related(
            'student', 'school_class'
        ).order_by('school_class', 'student__name')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "classes": SchoolClass.objects.all()
        })
        return context

class EnrollmentDetailView(PermissionRequiredMixin, DetailView):
    permission_required = "academics.view_enrollment"
    model = Enrollment
    template_name = 'academics/enrollments/detail.html'
    context_object_name = 'enrollment'

    def get_session_lookup(self):
        session_totals = (
            Session.objects.filter(
                subject_class__school_class_id=self.object.school_class_id
            )
            .annotate(
                teacher_code=F("subject_class__teacher__code"),
                subject_name=F("subject_class__subject__name"),
            )
            .values("teacher_code", "subject_name")
            .annotate(total=Count("id"))
        )
        session_lookup = {
            (row["teacher_code"], row["subject_name"]): row["total"]
            for row in session_totals
        }
        return session_lookup

    def get_attendance_report(self):
        queryset = (
            Attendance.objects.filter(
                student=self.object.student,
                status=Attendance.PRESENT,
                session__subject_class__school_class__academic_year=get_academic_year(self.request),
            )
            .annotate(
                teacher_code=F("session__subject_class__teacher__code"),
                subject_name=F("session__subject_class__subject__name"),
            )
            .values("teacher_code", "subject_name")
            .annotate(present_count=Count("id"))
        )

        data = {
            "subjects": {"zTotal", "zz%"},
            "counts": {"out of": {"zTotal": 0, "zz%": 100}, "subjects": {"zTotal": 0, "zz%": 0}}
        }
        session_lookup = self.get_session_lookup()
        for row in queryset:
            subject_name = row["subject_name"]
            teacher_code = row["teacher_code"]
            subject_full = f"{subject_name} ({teacher_code})"
            present_count = row["present_count"]

            data["subjects"].add(subject_full)

            data["counts"]["subjects"][subject_full] = present_count
            data["counts"]["subjects"]["zTotal"] += present_count

            session_total = session_lookup.get(
                (teacher_code, subject_name),
                0,
            )
            data["counts"]["out of"][subject_full] = session_total
            data["counts"]["out of"]["zTotal"] += session_total

        if data["counts"]["out of"]["zTotal"] > 0:
            data["counts"]["subjects"]["zz%"] = round(
                (data["counts"]["subjects"]["zTotal"] / data["counts"]["out of"]["zTotal"]) * 100
            )
        data["subjects"] = sorted(data["subjects"])

        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            "attendance_report": self.get_attendance_report(),
        })
        return context


class EnrollmentCreateView(PermissionRequiredMixin, CreateView):
    permission_required = "academics.add_enrollment"
    model = Student
    form_class = EnrollmentForm
    template_name = 'academics/enrollments/form.html'
    success_url = reverse_lazy('academics:enrollment:list')

    def get_initial(self):
        initial = super().get_initial()
        if self.request.GET.get('schoolclass'):
            initial.update({
                "school_class": SchoolClass.objects.get(id=self.request.GET.get('schoolclass')),
                "admission_date": timezone.localdate(),
            })
        return initial

    def get_success_url(self):
        if self.request.GET.get('schoolclass'):
            return reverse_lazy('academics:schoolclass:detail', kwargs={'pk': self.request.GET.get('schoolclass')})
        return super().get_success_url()

    def form_valid(self, form):
        with transaction.atomic():
            self.object = form.save()
            Enrollment.objects.create(
                school_class=form.cleaned_data['school_class'],
                student=self.object,
            )
        return redirect(self.get_success_url())


class EnrollmentUpdateView(PermissionRequiredMixin, RedirectToDetail, UpdateView):
    permission_required = "academics.change_enrollment"
    model = Student
    form_class = EnrollmentForm
    template_name = 'academics/enrollments/form.html'
    success_url = reverse_lazy('academics:enrollment:list')

    def get_initial(self):
        initial = super().get_initial()
        initial.update({
            "school_class": SchoolClass.objects.get(id=Enrollment.objects.get(student=self.object).school_class.id),
        })
        return initial

    def get_detail_url(self):
        return reverse_lazy('academics:enrollment:detail', kwargs={'pk': self.object.pk})

    def get_success_url(self):
        if self.request.GET.get('schoolclass'):
            return reverse_lazy('academics:schoolclass:detail', kwargs={'pk': self.request.GET.get('schoolclass')})
        return super().get_success_url()

    def form_valid(self, form):
        with transaction.atomic():
            self.object = form.save()
            Enrollment.objects.filter(
                student=self.object,
            ).update(school_class=form.cleaned_data['school_class'])
        return redirect(self.get_success_url())


class EnrollmentDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = "academics.delete_enrollment"
    http_method_names = ('post',)
    model = Enrollment
    success_url = reverse_lazy('academics:enrollment:list')

    def get_detail_url(self):
        return reverse_lazy('academics:enrollment:detail', kwargs={'pk': self.object.pk})

    def get_success_url(self):
        if self.request.GET.get('schoolclass'):
            return reverse_lazy('academics:schoolclass:detail', kwargs={'pk': self.request.GET.get('schoolclass')})
        return super().get_success_url()


class EnrollmentChangeLeaveStatusView(PermissionRequiredMixin, SingleObjectMixin, RedirectView):
    permission_required = "academics.change_enrollment"
    model = Enrollment

    def get_redirect_url(self, *args, **kwargs):
        return reverse_lazy('academics:schoolclass:detail', kwargs={'pk': self.object.school_class.id})

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.on_leave = not self.object.on_leave
        self.object.save()
        return super().get(request, args, kwargs)
