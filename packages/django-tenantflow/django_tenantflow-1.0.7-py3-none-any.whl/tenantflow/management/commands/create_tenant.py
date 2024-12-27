from django.core.management.base import BaseCommand
from django.db import connection
from django.core.management import call_command
from django.conf import settings
from django.apps import apps


class Command(BaseCommand):
    help = "Create a new tenant in the database"

    def add_arguments(self, parser):
        parser.add_argument('schema_name', type=str, help="Schema name for the tenant")
        parser.add_argument('tenant_name', type=str, help="Tenant name")

    def handle(self, *args, **kwargs):
        schema_name = kwargs['schema_name']
        tenant_name = kwargs['tenant_name']

        # Get the account model from settings.py
        account_model_path = getattr(settings, 'TENANTFLOW_ACCOUNT_MODEL', None)
        if not account_model_path:
            self.stderr.write(self.style.ERROR("[TenantFlow] 'TENANTFLOW_ACCOUNT_MODEL' is not defined in settings.py."))
            return
        
        try:
            Account = apps.get_model(account_model_path)
            
        except LookupError:
            self.stderr.write(self.style.ERROR(f"[TenantFlow] Invalid model path '{account_model_path}' in 'TENANTFLOW_ACCOUNT_MODEL'."))
            return

        # Create a new schema in the database
        self.stdout.write(f"[TenantFlow] Creating schema '{schema_name}'...")
        with connection.cursor() as cursor:
            cursor.execute(f"CREATE SCHEMA {schema_name}")

        # Create a new tenant in the 'Account' table
        tenant = Account.objects.create(
            schema_name=schema_name,
            name=tenant_name,
            domain=None
        )

        # Migrate the new schema
        with connection.cursor() as cursor:
            cursor.execute(f"SET search_path TO {schema_name}")
            call_command('migrate')
            self.stdout.write(f"[TenantFlow] Migrated schema '{schema_name}' successfully.")

        self.stdout.write(self.style.SUCCESS(f"[TenantFlow] Tenant '{tenant_name}' created successfully."))
