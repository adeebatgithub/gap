from django.core.cache import cache
from django.views.decorators.cache import cache_page

from academics.academicyear.models import AcademicYear


def get_academic_years():
    years = cache.get("academic_years")
    if years is None:
        years = AcademicYear.objects.only("id", "name", "is_active")
        cache.set("academic_years", years, timeout=60 * 15)

    return years

def global_data(request):
    return {
        "ACADEMIC_YEARS": get_academic_years(),
    }
