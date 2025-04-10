from django.http import JsonResponse
from .permissions import BasePermission

class PermissionMixin:
    """
    A mixin to apply permission checks to views.
    Override the `permission_classes` attribute in the view class.
    """
    permission_classes = []  # A list of permission classes to be checked

    def dispatch(self, request, *args, **kwargs):
        """
        Override the dispatch method to check permissions before proceeding with the view.
        """
        for permission in self.permission_classes:
            permission_checker = permission()
            if not permission_checker.has_permission(request, self):
                # If any permission check fails, return a 403 Forbidden response
                return JsonResponse({"error": "Permission denied."}, status=403)

        # Proceed to the original view logic if permission checks pass
        return super().dispatch(request, *args, **kwargs)
