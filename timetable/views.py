from django.contrib import messages
from django.db import transaction
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import TemplateView, View

from academics.models import SubjectClass, SchoolClass
from timetable.models import Timetable, TimetableClass, TimetablePeriod, TimetableCell


class TimetableView(TemplateView):
    template_name = "timetable/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "subjects": SubjectClass.objects.all(),
            "timetable": Timetable.objects.last(),
            "school_classes": SchoolClass.objects.all(),
        })
        return context


class TimetableUpsertView(View):
    def post(self, request, *args, **kwargs):
        class_names = request.POST.getlist('class_names[]')
        period_numbers = request.POST.getlist('period_numbers[]')
        period_names = request.POST.getlist('period_names[]')
        cells = request.POST.getlist('timetable_cells[]')

        with transaction.atomic():
            timetable = Timetable.objects.filter(created_at=timezone.localdate())
            if timetable.exists():
                timetable = timetable.first()
                timetable.classes.all().delete()
                timetable.periods.all().delete()
                timetable.cells.all().delete()
            else:
                timetable = Timetable.objects.create()

            for cls in class_names:
                TimetableClass.objects.create(timetable=timetable, school_class_id=cls)

            for num, name in zip(period_numbers, period_names):
                TimetablePeriod.objects.create(timetable=timetable, number=num, time_range=name)

            for p_idx, p_num in enumerate(period_numbers):
                for c_idx, cls in enumerate(class_names):
                    cell_index = p_idx * len(class_names) + c_idx
                    TimetableCell.objects.create(
                        timetable=timetable,
                        period_number=p_num,
                        school_class_id=cls,
                        subject_class_id=cells[cell_index]
                    )

        messages.success(request, "Timetable Saved")
        return redirect(reverse_lazy('timetable:index'))
