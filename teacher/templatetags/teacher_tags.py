from django import template

from academics.models import Teacher

register = template.Library()


@register.filter
def get_teacher_id(user):
    return Teacher.objects.get(user=user).id
