from django.contrib import admin
from academics.models import *


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('user__first_name',)


@admin.register(SchoolClass)
class SchoolClassAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name',)


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


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('date', 'subject', 'school_class')
    list_filter = ('date',)


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'session', 'status')
    list_filter = ('session__date', 'session__subject')
