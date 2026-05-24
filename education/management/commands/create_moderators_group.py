from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):
    help = 'Создаёт группу модераторов с правами'


    def handle(self, *args, **options):
        moderators_group, created = Group.objects.get_or_create(name='moderators')
        if created:
            self.stdout.write(self.style.SUCCESS(f'Группа {moderators_group.name} создана'))
        else:
            self.stdout.write(self.style.WARNING(f'Группа {moderators_group.name} уже существует'))


        permissions = []
        for perm in ['view_course', 'change_course', 'view_lesson', 'change_lesson']:
            perm_obj = Permission.objects.get(codename=perm)
            permissions.append(perm_obj)

        moderators_group.permissions.add(*permissions)
        self.stdout.write(self.style.SUCCESS(f'Права группы {moderators_group.name}:'))
        for perm in moderators_group.permissions.all():
            self.stdout.write(f'- {perm.name}')
