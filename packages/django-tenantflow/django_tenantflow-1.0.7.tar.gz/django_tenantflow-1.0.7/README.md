# Configuración de Django Multitenant


1. Instalación de Django y creación de proyecto y app.

```bash 
pip install django
django-admin startproject myproject
python manage.py startapp baseapp
cd myproject
```

2. Instalación de django-tenantflow.

```bash
pip install django-tenantflow
``` 

3. Configuración de la aplicación.

```python
INSTALLED_APPS = [
    ...
    'tenantflow',
    'baseapp',
    ...
]
```

4. Agregar el middleware de tenantflow.

```python
MIDDLEWARE = [
    ...
    'tenantflow.middleware.TenantMiddleware',
    ...
]
```

5. Configuraciones de la librería.

```python

TENANTFLOW_DEFAULT_SCHEMA = 'public'  # Esquema predeterminado
TENANTFLOW_VALIDATION = True         # Habilitar validación de acceso al tenant
TENANTFLOW_SWITCH_METHOD = 'session' # Métodos disponibles: session, subdomain, header
TENANTFLOW_ACCOUNT_MODEL = "baseapp.Account" # Modelo de cuenta
```

6. Crear modelos para cuentas y usuarios.

```python
from tenantflow.models import AbstractAccount, AbstractUserAccount

class Account(AbstractAccount):
    pass

class UserAccount(AbstractUserAccount):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
```

7. Aplicar migraciones al esquema público.

```bash
python manage.py makemigrations
python manage.py migrate
```
