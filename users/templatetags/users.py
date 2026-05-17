from django import template

register = template.Library()


@register.filter
def has_group(user, group_name):
    print(group_name, user)
    return user.groups.filter(name=group_name).exists()
