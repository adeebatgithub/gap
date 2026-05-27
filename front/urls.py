from django.urls import path, include

from . import views, gallery

urlpatterns = [
    path('',views.HomeView.as_view(),name='home'),
    path('about/',views.AboutView.as_view(),name='about'),
    path('activity/',views.ActivitiesView.as_view(),name='activity'),
    path('application/',views.ApplicationView.as_view(),name='application'),
    path('contact/',views.ContactView.as_view(),name='contact'),
    path('program/',views.ProgramView.as_view(),name='program'),
    path('womens_academy/',views.WomenAcademyView.as_view(),name='womens_academy'),

    path('inquiry/list/',views.InquiryListView.as_view(),name='inquiry-list'),
    path('inquiry/detail/<int:pk>/',views.InquiryDetailView.as_view(),name='inquiry-detail'),
    path('inquiry/delete/<int:pk>/',views.InquiryDeleteView.as_view(),name='inquiry-delete'),
    path('gallery/', include('front.gallery.urls')),
]