from contextlib import contextmanager
from django.db import connection
from tenantflow.models import AbstractAccount

@contextmanager
def switch_schema(schema_name):
    """
    Context manager that changes the schema search path to the given schema name.
    """
    with connection.cursor() as cursor:
        cursor.execute("SHOW search_path")
        original_schema = cursor.fetchone()[0]

    try:
        with connection.cursor() as cursor:
            cursor.execute(f"SET search_path TO {schema_name}")

        yield

    finally:
        with connection.cursor() as cursor:
            cursor.execute(f"SET search_path TO {original_schema}")


def get_active_tenant(request):
    """
    Returns the tenant that is currently active in the request session.
    """
    tenant_id = request.session.get('tenant_id')
    if not tenant_id:
        return None
    
    return AbstractAccount.objects.filter(id=tenant_id).first()


def schema_exists(schema_name):
    """
    Validates if the given schema name exists in the database.
    """
    with connection.cursor() as cursor:
        cursor.execute("SELECT schema_name FROM information_schema.schemata WHERE schema_name = %s", [schema_name])
        return cursor.fetchone() is not None
    