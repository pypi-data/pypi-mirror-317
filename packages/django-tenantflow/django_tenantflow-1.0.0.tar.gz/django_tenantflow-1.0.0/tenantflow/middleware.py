from django.conf import settings
from django.db import connection
from django.contrib.auth import logout
from django.shortcuts import redirect
from tenantflow.models import AbstractAccount, AbstractUserAccount

class TenantMiddleware:
    """
    Middleware to manage the current tenant in multitenant projects.
    Adjusts the `search_path` of PostgreSQL according to the active tenant.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        
        # From settings.py
        self.default_schema = getattr(settings, 'TENANTFLOW_DEFAULT_SCHEMA', 'public')
        self.validation_enabled = getattr(settings, 'TENANTFLOW_VALIDATION', True)
        self.switch_method = getattr(settings, 'TENANTFLOW_SWITCH_METHOD', 'session')   # session, subdomain, header

    def __call__(self, request):
        
        tenant_id = self._get_tenant_id(request)
        user = request.user

        if user.is_authenticated and tenant_id:

            try:
                
                # Validate if the user has access to the tenant
                tenant = AbstractAccount.objects.get(id=tenant_id)
                if self.validation_enabled and not self._user_has_access(user, tenant):
                    raise AbstractAccount.DoesNotExist

                # Set the `search_path` to the tenant schema
                with connection.cursor() as cursor:
                    cursor.execute(f"SET search_path TO {tenant.schema_name}")
                    request.tenant = tenant

            except AbstractAccount.DoesNotExist:
                logout(request)
                return redirect('login')

        response = self.get_response(request)

        # Reset the `search_path` to the default schema
        with connection.cursor() as cursor:
            cursor.execute(f"SET search_path TO {self.default_schema}")
        
        return response

    def _get_tenant_id(self, request):
        """
        Get the tenant ID from the specified method.
        """
        if self.switch_method == 'session':
            return request.session.get('tenant_id')
        
        elif self.switch_method == 'subdomain':
            host = request.get_host().split('.')
            return AbstractAccount.objects.filter(domain=host[0]).first().id if len(host) > 1 else None
        
        elif self.switch_method == 'header':
            return request.headers.get('X-Tenant-ID')
        
        else:
            raise ValueError(f"Invalid switch method: {self.switch_method}. Use 'session', 'subdomain' or 'header'.")

    def _user_has_access(self, user, tenant):
        """
        Validate if the user has access to the tenant.
        """
        return AbstractUserAccount.objects.filter(user=user, AbstractAccount=tenant).exists()
