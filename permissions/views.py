
from django.views import View
from django.http import JsonResponse
from .models import UserRole, Role, User
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from permissions.permissions import HasRolePermission
from .forms import RoleForm
from .mixins import PermissionMixin
import json
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
        
class AssignRoleView(PermissionMixin, View):
    permission_classes = [HasRolePermission]

    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        user_id = data.get("user_id")
        role_id = data.get("role_id")

        user = get_object_or_404(User, id=user_id)
        role = get_object_or_404(Role, id=role_id)

        user_role_perm, _ = UserRole.objects.get_or_create(user=user)
        user_role_perm.role = role
        user_role_perm.save()

        return JsonResponse({"message": "Role assigned successfully."}, status=200)
        

@method_decorator(csrf_exempt, name='dispatch')
class CreateRoleView(PermissionMixin, View):
    permission_classes = [HasRolePermission]

    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        form = RoleForm(data=data)

        if form.is_valid():
            cleaned_data = form.cleaned_data
            if Role.objects.filter(name=cleaned_data.get("name")).exists():
                raise ValidationError("Role with this name already exists.")
            form.save()

            
            response_data = {
                "message": "Role created successfully!",
                "data": form.cleaned_data
            }
            return JsonResponse(response_data, status=200)
        
        # Log or print form errors for debugging
        print("Form errors:", form.errors)  # You can log it to a file instead of printing

        # Respond with the errors to understand why the form is invalid
        return JsonResponse({"message": "Invalid Data", "errors": form.errors}, status=400)



@method_decorator(csrf_exempt, name='dispatch')
class UpdateRoleView(PermissionMixin, View):
    permission_classes = [HasRolePermission]

    def patch(self, request):
        data = json.loads(request.body.decode('utf-8'))
        role_id = data.get("role_id")
        if not role_id:
            return JsonResponse({"error": "Role ID is required!"}, status=400)

        role = get_object_or_404(Role, id=role_id)
        
        # Pass the instance (role) to update it and use data for the updated values
        form = RoleForm(data=data, instance=role)

        if form.is_valid():
            form.save()
            return JsonResponse({"message": "Role updated successfully!", "data": form.cleaned_data}, status=200)
        return JsonResponse({"message": "Invalid Data", "errors": form.errors}, status=400)

        
@method_decorator(csrf_exempt, name='dispatch')    
class DeleteRoleView(PermissionMixin, View):
    permission_classes = [HasRolePermission]

    def delete(self, request):
        data = json.loads(request.body.decode('utf-8'))
        role_id = data.get("role_id")
        if not role_id:
            return JsonResponse({"error": "Role ID is required!"}, status=400)

        role = get_object_or_404(Role, id=role_id)
        role.delete()
        return JsonResponse({"message": "Role deleted successfully!"}, status=200)