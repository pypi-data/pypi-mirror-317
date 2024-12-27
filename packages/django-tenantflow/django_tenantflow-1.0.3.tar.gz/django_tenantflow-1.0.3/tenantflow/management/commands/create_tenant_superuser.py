from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from tenantflow.models import AbstractAccount, AbstractUserAccount


class Command(BaseCommand):
    help = "Create a superuser and associate it to a tenant."

    def add_arguments(self, parser):
        parser.add_argument('schema_name', type=str, help="Schema name of the tenant")
        parser.add_argument('username', type=str, help="Username of the superuser")
        parser.add_argument('email', type=str, help="Email of the superuser")
        parser.add_argument('password', type=str, help="Password of the superuser")

    def handle(self, *args, **kwargs):
        schema_name = kwargs['schema_name']
        username = kwargs['username']
        email = kwargs['email']
        password = kwargs['password']

        # Validate if the schema exists
        account_model = AbstractAccount
        tenant = account_model.objects.filter(schema_name=schema_name).first()

        if not tenant:
            self.stderr.write(self.style.ERROR(f"[TenantFlow] Schema '{schema_name}' does not exist."))
            return

        # Create the superuser
        try:

            if User.objects.filter(username=username).exists():
                self.stderr.write(self.style.ERROR(f"[TenantFlow] Username '{username}' already exists."))
                return

            superuser = User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f"[TenantFlow] Superuser '{username}' created."))

            # Associate the superuser to the tenant
            user_account_model = AbstractUserAccount
            user_account_model.objects.create(user=superuser, account=tenant)
            self.stdout.write(self.style.SUCCESS(f"[TenantFlow] Superuser '{username}' associated to tenant '{schema_name}'."))

        except Exception as e:
            self.stderr.write(self.style.ERROR(f"[TenantFlow] Error creating superuser: {e}."))
