from django.db import models

class AbstractAccount(models.Model):
    """
    Abstract model to define the structure of a tenant or account.
    """
    name = models.CharField(max_length=255, help_text="Tenant name")
    schema_name = models.CharField(
        max_length=63, unique=True, help_text="Schema name associated with the tenant"
    )
    domain = models.CharField(
        blank=True, null=True, max_length=255, unique=True, help_text="Domain name associated with the tenant"
    )
    created_at = models.DateTimeField(auto_now_add=True, help_text="Creation date")
    updated_at = models.DateTimeField(auto_now=True, help_text="Last update date")

    def __str__(self):
        return self.name

    class Meta:
        abstract = True
        verbose_name = "Tenant"
        verbose_name_plural = "Tenants"