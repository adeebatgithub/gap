from django import template

from teacher.teacher.models import Teacher

register = template.Library()


@register.filter
def get_teacher_id(user):
    return Teacher.objects.get(user=user).id

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def remove_z(header):
    if header[0] == "z":
        return header.replace("z", "")
    return header
