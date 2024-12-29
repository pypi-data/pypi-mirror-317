# ACLVL Permissions

**ACLVL Permissions** is a Django package that provides an easy-to-use system for managing roles and access levels within your Django applications. It simplifies role-based access control (RBAC) by linking roles to access levels and associating them with views.

---

## Features

- Define roles and access levels for flexible and scalable RBAC.
- Automatically create or retrieve `AccessLevel` objects from views with declared permissions.
- Management commands to list views and synchronize access levels.
- Django admin integration for managing roles and access levels.

---

## Installation

1. Install the package using pip:
```bash
pip install aclvl_permissions
```
2. Add the app to your INSTALLED_APPS in settings.py:
```bash
INSTALLED_APPS = [
    # Other apps
    'aclvl_permissions',
]
```

4. Run migrations to set up the database models:
```bash
python manage.py makemigrations aclvl_permissions
python manage.py migrate
```


## Models

### Role

The 'Role' model defines user roles within the system. Each role can be associated with multiple 'AccessLevel' objects.

# ACLVL Permissions Models

The **ACLVL Permissions** package provides two primary models: `Role` and `AccessLevel`. These models form the backbone of the role-based access control (RBAC) system by defining roles and permissions within your application.

---

## Models Overview

### 1. Role

The `Role` model represents a user role within the system. Roles are linked to `AccessLevel` objects to define what permissions a role has.

#### Fields

| Field          | Type            | Description                                   |
|-----------------|-----------------|-----------------------------------------------|
| `name`         | `CharField`     | Name of the role (e.g., "Admin", "Editor").  |
| `role_key`     | `CharField`     | Unique identifier key for the role.          |
| `access_level` | `ManyToManyField` | Relationship to the `AccessLevel` model.     |

### 2. AccessLevel

The 'AccessLevel' model represents an individual permission within the system. Access levels are linked to roles to grant specific permissions.

#### Fields

| Field          | Type            | Description                                   |
|-----------------|-----------------|-----------------------------------------------|
| `name`         | `CharField`     | Name of the role (e.g., "Admin", "Editor").  |
| `access_key`     | `CharField`     | Unique identifier key for the access level. |

## Commands Overview

### 1. `list_views`

The `list_views` command lists all declared views in your Django project, displays their `view_key` and `required_access_levels`, and ensures that all `AccessLevel` objects for the specified `required_access_levels` are created in the database.

#### Features:
- Lists all views with a `view_key` and `required_access_levels`.
- Automatically creates or retrieves `AccessLevel` objects based on declared permissions.

#### Command Usage:
```bash
python manage.py aclvl_set_view_keys
```

## Usage
In your Django project, you can use the custom permission as follows:

```bash
from my_django_permissions.permissions import AccessLevelPermission

class MyView(APIView):
    permission_classes = [AccessLevelPermission]
    required_access_levels = ['view_all_model', 'view_owner_model', 'create_all_model']
    view_key = 'model'
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

