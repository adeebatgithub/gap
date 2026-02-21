from django.conf import settings


def global_data(request):
    return {
        "PROJECT_NAME": getattr(settings, "PROJECT_NAME") or "Project",
    }
