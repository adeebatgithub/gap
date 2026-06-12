from django.core.cache import cache


def get_groups(request):
    user_groups = cache.get("user_groups")
    if user_groups is None and request.user.is_authenticated:
        user_groups = (request.user.groups.values_list("name", flat=True))
        cache.set("user_groups", user_groups, timeout=60 * 15)

    return user_groups


def global_data(request):
    return {
        "USER_GROUPS": get_groups(request),
    }
