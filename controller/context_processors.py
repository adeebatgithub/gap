from django.conf import settings
from django.utils import timezone


def global_data(request):
    return {
        "PROJECT_NAME": getattr(settings, "PROJECT_NAME") or "Project",
        "TODAY": timezone.localdate()
    }
