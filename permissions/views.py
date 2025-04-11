
from django.views import View
from django.http import JsonResponse
from .models import Role, Permission
from accounts.models import CustomUser
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from permissions.permissions import HasRolePermission
from .forms import RoleForm
from .mixins import PermissionMixin
import json
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


 

@method_decorator(csrf_exempt, name='dispatch')
class AssignRoleView(PermissionMixin, View):
    permission_classes = [HasRolePermission]

    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        user_id = data.get("user_id")
        role_id = data.get("role_id")
        
        user = get_object_or_404(CustomUser, id=user_id)
        role = get_object_or_404(Role, id=role_id)
        
        # if user.role is not None:
        #     return JsonResponse({"message": "User already has a role. You can update his role now."}, status=400)

        user.role = role
        user.save()
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
        role_name = data.get("name")
        if not role_name:
            return JsonResponse({"error": "Role Name is required!"}, status=400)

        role = get_object_or_404(Role, name=role_name)
        
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
    
@method_decorator(csrf_exempt, name='dispatch')
class DeleteUserRoleView(PermissionMixin, View):
    permission_classes = [HasRolePermission]

    def delete(self, request):
        data = json.loads(request.body.decode('utf-8'))
        user_id = data.get("user_id")
        if not user_id:
            return JsonResponse({"error": "User ID is required!"}, status=400)

        user = get_object_or_404(CustomUser, id=user_id)
        user.role = None
        user.save()
        return JsonResponse({"message": "User role deleted successfully!"}, status=200)
    
@method_decorator(csrf_exempt, name='dispatch')
class ListRoleView(View):
    def get(self, request):
        roles = Role.objects.all()
        roles_list = [{"id": role.id, "name": role.name} for role in roles]
        return JsonResponse({"roles": roles_list}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class ListPermissionView(View):
    def get(self, request):
        permissions = Permission.objects.all().order_by('id')
        permissions_list = [{"id": permission.id, "name": permission.name, "codename": permission.codename} for permission in permissions]
        return JsonResponse({"permissions": permissions_list}, status=200)