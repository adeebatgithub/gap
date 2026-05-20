from academics.schoolclass import views as schoolclass_views
from academics.schoolclass.models import SchoolClass
from academics.subject.models import SubjectClass


class SchoolClassListView(schoolclass_views.SchoolClassListView):
    template_name = 'teacher/schoolclass/list.html'

    def get_queryset(self):
        return SchoolClass.objects.filter(
            id__in=SubjectClass.objects.filter(teacher__user=self.request.user).values_list('id', flat=True))


class SchoolClassDetailView(schoolclass_views.SchoolClassDetailView):
    template_name = 'teacher/schoolclass/detail.html'
