from django import forms
from .models import Role, Permission

class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = ['id', 'name', 'permissions']

    def clean_permissions(self):
        permissions = self.cleaned_data.get('permissions')
        if not isinstance(permissions, list):
            raise forms.ValidationError("Permissions must be a list.")
        
        return permissions
    
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name:
            raise forms.ValidationError("Role name is required.")
        
        return name

    