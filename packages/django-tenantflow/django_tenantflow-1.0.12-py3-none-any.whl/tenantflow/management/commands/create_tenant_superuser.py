from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import connection
from django.conf import settings
from django.apps import apps


class Command(BaseCommand):
    help = "Create a superuser in the public schema and associate it with a specific tenant"

    def add_arguments(self, parser):
        parser.add_argument('schema_name', type=str, help="Schema name for the tenant")
        parser.add_argument('username', type=str, help="Username for the superuser")
        parser.add_argument('email', type=str, help="Email address for the superuser")
        parser.add_argument('password', type=str, help="Password for the superuser")

    def handle(self, *args, **kwargs):
        schema_name = kwargs['schema_name']
        username = kwargs['username']
        email = kwargs['email']
        password = kwargs['password']

        # Obtener el modelo concreto de Account
        account_model_path = getattr(settings, 'TENANTFLOW_ACCOUNT_MODEL', None)
        if not account_model_path:
            self.stderr.write(self.style.ERROR("TENANTFLOW_ACCOUNT_MODEL is not defined in settings.py"))
            return

        try:
            Account = apps.get_model(account_model_path)
        except LookupError:
            self.stderr.write(self.style.ERROR(f"Invalid TENANTFLOW_ACCOUNT_MODEL: {account_model_path}"))
            return

        # Validar si el esquema del tenant existe
        tenant = Account.objects.filter(schema_name=schema_name).first()
        if not tenant:
            self.stderr.write(self.style.ERROR(f"Schema '{schema_name}' does not exist."))
            return

        # Cambiar al esquema público para crear el usuario
        self.stdout.write(f"[TenantFlow] Switching to public schema...")
        with connection.cursor() as cursor:
            cursor.execute("SET search_path TO public")

        User = get_user_model()
        if User.objects.filter(username=username).exists():
            self.stderr.write(self.style.ERROR(f"User '{username}' already exists in the public schema."))
            return

        # Crear el superusuario en el esquema público
        self.stdout.write(f"[TenantFlow] Creating superuser '{username}' in the public schema...")
        superuser = User.objects.create_superuser(username=username, email=email, password=password)

        # Asociar el superusuario al tenant mediante UserAccount
        user_account_model_path = getattr(settings, 'TENANTFLOW_USERACCOUNT_MODEL', None)
        if not user_account_model_path:
            self.stderr.write(self.style.ERROR("TENANTFLOW_USERACCOUNT_MODEL is not defined in settings.py"))
            return

        try:
            UserAccount = apps.get_model(user_account_model_path)
        except LookupError:
            self.stderr.write(self.style.ERROR(f"Invalid TENANTFLOW_USERACCOUNT_MODEL: {user_account_model_path}"))
            return

        UserAccount.objects.create(user=superuser, account=tenant)

        self.stdout.write(self.style.SUCCESS(
            f"[TenantFlow] Superuser '{username}' created successfully in the public schema and associated with tenant '{schema_name}'."
        ))
