from django.apps import apps
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.db import transaction


class Command(BaseCommand):
    ROLE_POLICY = {
        "Admin": "__all__",
        "Teacher": {
            "academics.Attendance": ["add", "change", "delete", "view"],
            "academics.Session": ["add", "change", "delete", "view"],
            "academics.Enrollment": ["view"],
            "academics.Teacher": ["view"],
            "academics.SchoolClass": ["view"],
        }
    }

    @transaction.atomic
    def handle(self, *args, **options):

        for role_name, policy in self.ROLE_POLICY.items():
            group, _ = Group.objects.get_or_create(name=role_name)

            group.permissions.clear()

            if policy == "__all__":
                group.permissions.set(Permission.objects.all())
                continue

            for model_path, actions in policy.items():
                app_label, model_name = model_path.split(".")

                model = apps.get_model(app_label, model_name)
                content_type = ContentType.objects.get_for_model(model)

                for action in actions:
                    permissions = Permission.objects.filter(
                        content_type=content_type,
                        codename__startswith=action
                    )
                    group.permissions.add(*permissions)

        self.stdout.write(self.style.SUCCESS("Roles configured successfully."))
