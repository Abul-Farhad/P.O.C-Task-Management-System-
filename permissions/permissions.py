from django.urls import resolve
from .models import UserRole
from django.core.exceptions import PermissionDenied

class BasePermission:
    """
    A base permission class that can be extended to define specific permissions.
    """
    def has_permission(self, request, view):
        raise NotImplementedError("Subclasses must implement the `has_permission` method.")

class HasRolePermission(BasePermission):
    """
    Custom permission to check if a user has the necessary role permission for the current view.
    """
    def has_permission(self, request, view):
        """
        Checks if the user has the appropriate permissions for the current view.
        """
        # Skip permission check for superusers or staff
        if request.user.is_superuser or request.user.is_staff:
            return True

        try:
            # Get the route name from the URL (equivalent to the 'codename' in DRF)
            route_name = resolve(request.path).url_name
        except Exception as e:
            # If route resolution fails, deny access
            raise PermissionDenied("Unable to resolve route.")
        
        # Get the user's role and associated permissions
        try:
            user_role = UserRole.objects.get(user=request.user)
            role_permissions = user_role.role.permissions  # This could be a list of codenames
        except UserRole.DoesNotExist:
            # If the user has no role, deny permission
            raise PermissionDenied("User does not have an assigned role.")

        # Check if the required route name (permission codename) is in the user's permissions
        if route_name not in role_permissions:
            raise PermissionDenied(f"Permission for '{route_name}' is not granted.")
        
        return True
