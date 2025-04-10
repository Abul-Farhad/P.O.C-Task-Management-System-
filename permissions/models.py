from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Permission(models.Model):
    codename = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.codename
    
class Role(models.Model):
    name = models.CharField(max_length=100, unique=True)
    permissions = models.JSONField(default=list, blank=True)

    def __str__(self):
        return self.name
    
    def has_permission(self, codename):
        return codename in self.permissions
    
class UserRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_roles')
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='user_roles')

    class Meta:
        unique_together = ('user', 'role')

    def __str__(self):
        return f"{self.user.email} - {self.role.name}"
    
