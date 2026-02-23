from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group

from users.models import User

USER_MODEL: User = get_user_model()


class Command(BaseCommand):
    help = 'Create a new user'

    def add_arguments(self, parser):
        parser.add_argument('role', type=str, help='role of user(root, admin)')

    def handle(self, *args, **kwargs):
        role = kwargs['role']

        if role == 'root':
            self.create_superuser()
            return

        d = {
            'admin': self.create_account,
            'teacher': self.create_account,
        }
        if role not in ['root', *d.keys()]:
            raise CommandError(f"role not found: {role}")
        d[role](role)

    def create_superuser(self):
        if not USER_MODEL.objects.filter(username='root').exists():
            USER_MODEL.objects.create_superuser(username='root', password='root')
            self.stdout.write(self.style.SUCCESS('Successfully created superuser: root'))
        else:
            self.stdout.write(self.style.WARNING('Superuser "root" already exists'))

    def create_account(self, role):
        _role = Group.objects.get(name=role.title()) or None
        if not _role:
            raise CommandError("group not found")

        admin = USER_MODEL.objects.create_user(username=role, password='1234', first_name=role.title(), last_name='user')
        admin.groups.add(_role)
        self.stdout.write(self.style.SUCCESS(f'Successfully created user({role}): {role}, pass: 1234'))
