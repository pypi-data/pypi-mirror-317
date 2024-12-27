from django.core.management.base import BaseCommand
from django.db import connection
from tenantflow.models import AbstractAccount


class Command(BaseCommand):
    help = "Delete a tenant from the database"

    def add_arguments(self, parser):
        parser.add_argument('schema_name', type=str, help="Schema name for the tenant to delete")

    def handle(self, *args, **kwargs):
        schema_name = kwargs['schema_name']

        # Validate if the tenant exists
        account_model = AbstractAccount
        tenant = account_model.objects.filter(schema_name=schema_name).first()

        if not tenant:
            self.stderr.write(self.style.ERROR(f"[TenantFlow] Tenant '{schema_name}' does not exist."))
            return

        # Delete the schema from the database
        self.stdout.write(f"[TenantFlow] Deleting schema '{schema_name}'...")
        with connection.cursor() as cursor:
            cursor.execute(f"DROP SCHEMA {schema_name} CASCADE")

        # Delete the tenant from the 'Account' table
        tenant.delete()

        self.stdout.write(self.style.SUCCESS(f"[TenantFlow] Tenant '{schema_name}' deleted successfully."))
