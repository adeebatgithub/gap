from django.db import models
from django.utils import timezone


class SoftDeleteQuerySet(models.QuerySet):
    def delete(self):
        return super().update(
            is_deleted=True,
            deleted_at=timezone.now(),
        )

    def hard_delete(self):
        return super().delete()


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return SoftDeleteQuerySet(self.model, using=self._db).filter(is_deleted=False)


class AllObjectsManager(models.Manager):
    """Includes deleted objects"""

    def get_queryset(self):
        return super().get_queryset()


class SoftDeleteModel(models.Model):
    is_deleted = models.BooleanField(default=False, editable=False, )
    deleted_at = models.DateTimeField(null=True, blank=True, editable=False, )

    objects = SoftDeleteManager()
    all_objects = AllObjectsManager()

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        """Soft delete"""
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save(update_fields=["is_deleted", "deleted_at"])

    def hard_delete(self, using=None, keep_parents=False):
        """Permanent delete"""
        super().delete(using=using, keep_parents=keep_parents)

    def restore(self):
        """Restore soft-deleted object"""
        self.is_deleted = False
        self.deleted_at = None
        self.save(update_fields=["is_deleted", "deleted_at"])


class TimeStampedModel(SoftDeleteModel):
    """
    Abstract base class with created/modified timestamps.

    - created_at: set once when created
    - updated_at: updated each save()
    Both fields are timezone-aware DateTimeFields and indexed for queries.
    """
    created_at = models.DateTimeField(
        default=timezone.now,
        editable=False,
        db_index=True,
        help_text="When this object was created (UTC)."
    )
    updated_at = models.DateTimeField(
        default=timezone.now,
        editable=False,
        db_index=True,
        help_text="When this object was last updated (UTC)."
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)
