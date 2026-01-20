from django.core.management.base import BaseCommand
from core.tasks import load_customers, load_loans

class Command(BaseCommand):
    help = 'Load initial data from Excel files'

    def handle(self, *args, **options):
        self.stdout.write('Loading customers...')
        load_customers.delay()
        self.stdout.write('Loading loans...')
        load_loans.delay()
        self.stdout.write('Data loading tasks queued.')