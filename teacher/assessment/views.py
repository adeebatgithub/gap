from django.contrib import messages
from django.db import transaction
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View

from academics.enrollment.models import Enrollment
from teacher.attendance.utils import get_leafnodes
from .forms import AssessmentForm, AssessmentUpdateForm
from .models import Assessment, Grade


class AssessmentListView(ListView):
    model = Assessment
    template_name = 'teacher/assessments/list.html'
    context_object_name = 'assessments'

    def get_filters(self):
        filters = {}
        if date:=self.request.GET.get('month'):
            year, month_num = date.split("-")
            filters.update({
                'date__month': month_num,
                'date__year': year,
            })
        else:
            filters.update({
                'date__month': timezone.localdate().month,
                'date__year': timezone.localdate().year,
            })

        return filters

    def get_template_names(self):
        if self.request.htmx:
            return ["teacher/assessments/partial_list.html"]
        return super().get_template_names()

    def get_queryset(self):
        return super().get_queryset().select_related(
            "subject_class",
            "subject_class__school_class",
            "subject_class__subject",
        ).filter(
            subject_class__teacher__user=self.request.user,
            **self.get_filters(),
        )


class AssessmentDetailView(DetailView):
    model = Assessment
    template_name = 'teacher/assessments/detail.html'
    context_object_name = 'assessment'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "grades": Grade.objects.select_related(
                "assessment",
                "student"
            ).filter(assessment=self.object).order_by('student__name'),
        })
        return context


class AssessmentCreateView(CreateView):
    model = Assessment
    form_class = AssessmentForm
    template_name = 'teacher/assessments/form.html'

    def get_success_url(self):
        return reverse_lazy('teacher:assessment:detail', kwargs={'pk': self.object.pk})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_initial(self):
        return {
            "date": timezone.localdate(),
        }

    def form_valid(self, form):
        with transaction.atomic():
            self.object = form.save()
            enrollments = Enrollment.objects.filter(
                school_class__in=get_leafnodes(self.object.subject_class.school_class)
            )
            for enrollment in enrollments:
                Grade.objects.create(
                    student_id=enrollment.student_id,
                    assessment=self.object,
                )
        return redirect(self.get_success_url())


class AssessmentUpdateView(UpdateView):
    model = Assessment
    form_class = AssessmentUpdateForm
    template_name = 'teacher/assessments/form.html'
    success_url = reverse_lazy('teacher:assessment:list')


class AssessmentDeleteView(DeleteView):
    http_method_names = ("post",)
    model = Assessment
    success_url = reverse_lazy('teacher:assessment:list')

    def delete(self, request, *args, **kwargs):
        Grade.objects.filter(assessment=self.object).delete()
        return super().delete(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return self.delete(request, *args, **kwargs)


class GradeAssessmentView(View):
    def get_object(self):
        return Assessment.objects.get(pk=self.kwargs['pk'])

    def get_success_url(self):
        return reverse_lazy('teacher:assessment:list')

    def post(self, request, *args, **kwargs):
        with transaction.atomic():
            assessment = self.get_object()
            grades = Grade.objects.filter(assessment=assessment)

            for grade in grades:
                mark = request.POST.get(f'grade_{grade.pk}')
                if int(mark) > assessment.mark:
                    messages.error(request, 'Mark cannot be greater than total mark')
                    return reverse_lazy('teacher:assessment:detail', kwargs={'pk': self.kwargs['pk']})
                grade.marks = int(mark)
                grade.save()
        messages.success(request, "Assessment saved successfully!")
        return redirect(self.get_success_url())
