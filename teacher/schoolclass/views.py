from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView, DetailView

from academics.models import SchoolClass, SubjectClass, Enrollment
from academics.schoolclass import views as schoolclass_views

class SchoolClassListView(schoolclass_views.SchoolClassListView):
    template_name = 'teacher/schoolclass/list.html'

    def get_queryset(self):
        return SchoolClass.objects.filter(id__in=SubjectClass.objects.filter(teacher__user=self.request.user).values_list('id', flat=True))


class SchoolClassDetailView(schoolclass_views.SchoolClassDetailView):
    template_name = 'teacher/schoolclass/detail.html'
