from django.contrib import messages
from django.db import transaction
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View

from academics.models import Assessment, Grade, Student, Enrollment
from .forms import AssessmentForm, AssessmentUpdateForm


class AssessmentListView(ListView):
    model = Assessment
    template_name = 'academics/assessments/list.html'
    context_object_name = 'assessments'


class AssessmentDetailView(DetailView):
    model = Assessment
    template_name = 'academics/assessments/detail.html'
    context_object_name = 'assessment'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "grades": Grade.objects.filter(assessment=self.object).order_by('student__reg_number'),
        })
        return context


class AssessmentCreateView(CreateView):
    model = Assessment
    form_class = AssessmentForm
    template_name = 'academics/assessments/form.html'
    success_url = reverse_lazy('academics:assessment:list')

    def form_valid(self, form):
        with transaction.atomic():
            self.object = form.save()
            students = Student.objects.filter(
                id__in=Enrollment.objects.filter(school_class=self.object.school_class).values("student_id")
            )
            for student in students:
                Grade.objects.create(
                    student=student,
                    assessment=self.object,
                )
        return redirect(self.get_success_url())


class AssessmentUpdateView(UpdateView):
    model = Assessment
    form_class = AssessmentUpdateForm
    template_name = 'academics/assessments/form.html'
    success_url = reverse_lazy('academics:assessment:list')


class AssessmentDeleteView(DeleteView):
    http_method_names = ("post",)
    model = Assessment
    success_url = reverse_lazy('academics:assessment:list')

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
        return reverse_lazy('academics:assessment:list')

    def post(self, request, *args, **kwargs):
        with transaction.atomic():
            assessment = self.get_object()
            grades = Grade.objects.filter(assessment=assessment)

            for grade in grades:
                mark = request.POST.get(f'grade_{grade.pk}')
                grade.marks = int(mark)
                grade.save()
        messages.success(request, "Assessment saved successfully!")
        return redirect(self.get_success_url())
