from django.contrib import admin

from teacher.assessment.models import Assessment, Grade
from teacher.attendance.models import Session, Attendance
from teacher.teacher.models import Teacher


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('user', "department")


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('date', 'subject_class__subject', 'subject_class__school_class')
    list_filter = ('date',)


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'session', 'status')
    list_filter = ('session__date', 'session__subject_class__subject')


@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = ("date", "subject", "school_class")


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ("id", "student", "marks")
