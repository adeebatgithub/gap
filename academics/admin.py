from django.contrib import admin
from academics.academicyear.models import AcademicYear
from academics.assessment.models import Assessment, Grade
from academics.enrollment.models import Student, Enrollment
from academics.schoolclass.models import SchoolClass
from academics.subject.models import Subject, SubjectClass


@admin.register(SchoolClass)
class SchoolClassAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')


@admin.register(SubjectClass)
class SubjectClassAdmin(admin.ModelAdmin):
    list_display = ('subject', 'school_class', 'teacher')


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'school_class', 'status', 'academic_year')
    list_filter = ('academic_year', 'school_class')


@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = ("date", "subject", "school_class")


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ("id", "student", "marks")
