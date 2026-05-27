# views.py
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)

from front.models import Gallery
from .forms import GalleryForm


class GalleryListView(PermissionRequiredMixin, ListView):
    permission_required = "front.view_gallery"
    model = Gallery
    template_name = "front/gallery/list.html"
    context_object_name = "images"

    def get_queryset(self):
        return super().get_queryset().order_by("position")


class GalleryCreateView(PermissionRequiredMixin, CreateView):
    permission_required = "front.add_gallery"
    model = Gallery
    form_class = GalleryForm
    template_name = "front/gallery/form.html"
    success_url = reverse_lazy("gallery:list")


class GalleryUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = "front.change_gallery"
    model = Gallery
    form_class = GalleryForm
    template_name = "front/gallery/form.html"
    success_url = reverse_lazy("gallery:list")


class GalleryDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = "front.delete_gallery"
    model = Gallery
    success_url = reverse_lazy("gallery:list")

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().delete(request, *args, **kwargs)