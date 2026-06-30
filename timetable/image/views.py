from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView

from .forms import TimetableImageForm
from timetable.models import TimetableImage


class TimetableImageListView(ListView):
    model = TimetableImage
    template_name = 'timetable/list.html'
    context_object_name = 'timetable_images'
    ordering = ['day']


class TimetableImageCreateView(CreateView):
    model = TimetableImage
    form_class = TimetableImageForm
    template_name = 'timetable/form.html'
    success_url = reverse_lazy('timetable:image:list')


class TimetableImageUpdateView(UpdateView):
    model = TimetableImage
    form_class = TimetableImageForm
    template_name = 'timetable/form.html'
    success_url = reverse_lazy('timetable:image:list')
