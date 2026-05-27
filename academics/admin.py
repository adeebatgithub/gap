from django.contrib import admin
from academics.academicyear.models import AcademicYear
from academics.enrollment.models import Student, Enrollment
from academics.schoolclass.models import SchoolClass
from academics.subject.models import Subject, SubjectClass
from academics.admission.models import Admission


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
    list_display = ('student', 'school_class', 'status', 'school_class__academic_year')
    list_filter = ('school_class__academic_year', 'school_class')


@admin.register(Admission)
class AdmissionAdmin(admin.ModelAdmin):
    list_display = ("full_name", "guardian_name", "district", "state")