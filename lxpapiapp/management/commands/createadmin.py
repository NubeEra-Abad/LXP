from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.core.management import call_command
class Command(BaseCommand):
    help = 'Create a superuser and a teacher with predefined credentials'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.NOTICE('Running makemigrations...'))
        call_command('makemigrations')

        self.stdout.write(self.style.NOTICE('Running migrate...'))
        call_command('migrate')
        
        User = get_user_model()

        # Creating the superuser
        username = 'admin'
        email = 'admin@example.com'
        password = 'admin123'  # Change this to your desired password

        self.stdout.write(self.style.WARNING(f'Creating Admin'))

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f'User "{username}" already exists.'))
        else:
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f'Superuser "{username}" created successfully.'))

        