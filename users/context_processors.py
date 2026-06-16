from django.core.cache import cache


def get_groups(request):
    user_groups = (request.user.groups.values_list("name", flat=True))
    return user_groups


def global_data(request):
    return {
        "USER_GROUPS": get_groups(request),
    }
