from django.core.management.base import BaseCommand
from users.models import Users


class Command(BaseCommand):
    help = 'Create a static admin user'

    def handle(self, *args, **kwargs):
        if not Users.objects.filter(username='admin').exists():
                admin_user = Users.objects.create_user(
                username='Admin',
                password='123456',  # Set the desired password for the admin user
                is_admin=True,
                # Set other admin-related fields here (e.g., first_name, last_name, etc.)
                first_name='Admin',
                last_name='Admin',
                email='admin@example.com',  # Add an email address for the admin user
                # Add other admin-related data as needed
            )
                self.stdout.write(self.style.SUCCESS('Successfully created admin user'))
        else:
            self.stdout.write(self.style.WARNING('Admin user already exists'))