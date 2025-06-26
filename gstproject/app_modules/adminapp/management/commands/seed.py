from django.apps import apps
from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.management import call_command
import sys
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    # help = 'Run makemigrations and migrate in one command.'
    help = "Seeds initial data for the application."
    
    def __init__(self):
        self.user_class = get_user_model()
        super().__init__()
        
    def handle(self, *args, **options):
        self.all_apps_make_migration()
        self.migrate()
        self.create_super_user()
        
    def create_super_user(self):
        if self.user_class.objects.filter(email=settings.SUPER_USER.get('ADMIN_EMAIL'),
                                          ).exists():
            self.stdout.write("Admin Account is already Created.")
            return False
        
        self.user_class.objects.create_superuser(
            username=settings.SUPER_USER.get('ADMIN_EMAIL'),
            email=settings.SUPER_USER.get('ADMIN_EMAIL'),
            password=settings.SUPER_USER.get('ADMIN_PASSWORD'),
            is_superuser = True,
        )
        self.stdout.write("Created {} admin account.".format(settings.SUPER_USER.get("ADMIN_EMAIL")))

    def all_apps_make_migration(self):
        for app in apps.get_app_configs():
            call_command("makemigrations",app.label)
            self.stdout.write("Created {} migration.".format(app.label))
            
            
    def migrate(self):
        call_command("migrate")