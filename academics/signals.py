from django.db.models.signals import post_save
from django.dispatch import receiver

from academics.models import AcademicYear

@receiver(post_save, sender=AcademicYear)
def set_active(sender, instance, created, **kwargs):
    if created:
        current_active = AcademicYear.objects.filter(is_active=True)
        current_active.update(is_active=False)
        instance.is_active = True
        instance.save()

