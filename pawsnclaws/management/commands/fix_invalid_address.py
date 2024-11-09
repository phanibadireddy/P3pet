from django.core.management.base import BaseCommand
from pawsnclaws.models import Address, register

class Command(BaseCommand):
    help = 'Fix invalid foreign keys in Address table'

    def handle(self, *args, **kwargs):
        invalid_addresses = Address.objects.exclude(user__in=register.objects.values('id'))
        count = invalid_addresses.count()
        invalid_addresses.delete()
        self.stdout.write(self.style.SUCCESS(f'Deleted {count} invalid address entries'))
