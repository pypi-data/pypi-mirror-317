from django.core.management.commands.migrate import Command as MigrateCommand
from django.db import connection
from tenantflow.models import AbstractAccount


class Command(MigrateCommand):
    help = "Apply migrations to all schemas, including the public schema"

    def handle(self, *args, **options):
    
        # Migrate the public schema
        self.stdout.write("[TenantFlow] Migrating public schema...")
        options['database'] = 'default'
        super().handle(*args, **options)

        # Get all tenants
        account_model = AbstractAccount
        tenants = account_model.objects.all()

        # Apply migrations to all schemas
        for tenant in tenants:
            self.stdout.write(f"[TenantFlow] Migrating schema '{tenant.schema_name}'...")

            try:
                with connection.cursor() as cursor:
                    cursor.execute(f"SET search_path TO {tenant.schema_name}")
                    super().handle(*args, **options)

            except Exception as e:
                self.stderr.write(f"[TenantFlow] Error migrating schema '{tenant.schema_name}': {e}.")

        # Reset the 'search_path' to the public schema
        with connection.cursor() as cursor:
            cursor.execute("SET search_path TO public")

        self.stdout.write(self.style.SUCCESS("[TenantFlow] All schemas migrated successfully."))
