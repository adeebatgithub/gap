from django.urls.base import reverse_lazy
from django.views.generic import TemplateView, ListView, DeleteView
from django.views.generic.detail import DetailView

from front.models import Gallery, Inquiry, Notification


class HomeView(TemplateView):
    template_name = "front/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "images": Gallery.objects.filter(position=Gallery.IN_HOME_PAGE).values("image")[:5],
            "notification": Notification.objects.last(),
        })
        return context


class AboutView(TemplateView):
    template_name = "front/about.html"


class ActivitiesView(TemplateView):
    template_name = "front/activities.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "tops": Gallery.objects.filter(position=Gallery.IN_TOP)[:5],
            "defaults": Gallery.objects.filter(position=Gallery.DEFAULT)[:5],
        })
        return context


class ApplicationView(TemplateView):
    template_name = "front/application.html"


class ContactView(TemplateView):
    template_name = "front/contact.html"


class ProgramView(TemplateView):
    template_name = 'front/programmes.html'


class WomenAcademyView(TemplateView):
    template_name = "front/womens_academy.html"


class NotificationsView(ListView):
    model = Notification
    template_name = "front/notification.html"
    context_object_name = "notifications"
    ordering = ['-date']


class InquiryListView(ListView):
    model = Inquiry
    context_object_name = "inquiries"
    template_name = ""

class InquiryDetailView(DetailView):
    model = Inquiry
    template_name = ""
    context_object_name = "inquiry"


class InquiryDeleteView(DeleteView):
    model = Inquiry
    success_url = reverse_lazy('inquiry-list')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().delete(request, *args, **kwargs)
