from django.db import models

class AppPermission(models.Model):
    class Meta:
        managed = False  # No database table needed
        default_permissions = ()
        permissions = [
            ("view_stats", "Can view stats"),
            ("view_admin_panel", "Can view Admin Panel"),
            ("view_exam_panel", "Can view Exam Panel"),
            ("view_danger", "Can view danger zone"),
        ]