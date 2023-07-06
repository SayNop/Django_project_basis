from rest_framework.permissions import DjangoModelPermissions


# Some permission class permission check:
# DjangoModelPermissions: POST, PUT, PATCH, DELETE
# IsAuthenticated: login user can do all request method

# request GET need permission check
class CustomPermissions(DjangoModelPermissions):

    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }
