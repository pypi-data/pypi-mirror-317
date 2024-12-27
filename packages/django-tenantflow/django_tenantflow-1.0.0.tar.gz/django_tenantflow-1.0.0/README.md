# Configuración de Django Multitenant
MULTITENANT_DEFAULT_SCHEMA = 'public'  # Esquema predeterminado
MULTITENANT_VALIDATION = True         # Habilitar validación de acceso al tenant
MULTITENANT_SWITCH_METHOD = 'session' # Métodos disponibles: session, subdomain, header


MIDDLEWARE = [
    ...
    'multitenant.middleware.TenantMiddleware',
    ...
]

from tenantflow.models import AbstractAccount

class Account(AbstractAccount):
    """
    Extended model for tenant account
    """
    plan = models.CharField(max_length=50, help_text="Plan contratado por el tenant")


from tenantflow.models import AbstractUserAccount

class UserAccount(AbstractUserAccount):
    """
    Relación extendida entre usuarios y tenants con datos adicionales.
    """
    extra_field = models.CharField(max_length=50, help_text="Campo adicional", blank=True)

from tenantflow.models import AbstractUserRole

class UserRole(AbstractUserRole):
    """
    Rol extendido con configuraciones específicas del proyecto.
    """
    additional_config = models.JSONField(blank=True, null=True, help_text="Configuraciones extra")


from tenantflow.models import AbstractUserPrivilege

class UserPrivilege(AbstractUserPrivilege):
    """
    Privilegios extendidos para casos de uso específicos.
    """
    restricted = models.BooleanField(default=False, help_text="Indica si este privilegio está restringido")

