from django.urls import path

from .views import (
    AssessmentListView,
    AssessmentDetailView,
    AssessmentCreateView,
    AssessmentUpdateView,
    AssessmentDeleteView,
    GradeAssessmentView
)

app_name = 'assessment'

urlpatterns = [
    path('', AssessmentListView.as_view(), name='list'),
    path('<int:pk>/', AssessmentDetailView.as_view(), name='detail'),
    path('create/', AssessmentCreateView.as_view(), name='create'),
    path('<int:pk>/update/', AssessmentUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', AssessmentDeleteView.as_view(), name='delete'),

    path('<int:pk>/grade/', GradeAssessmentView.as_view(), name='grade'),
]
