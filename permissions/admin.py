from django.contrib import admin
from permissions.models import Role, Permission



# Register your models here.
class RoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'permissions')
    # Assuming permissions is a JSONField, you might want to display it differently
 
    list_filter = ('name',)
    search_fields = ('name',)
    ordering = ('name',)
    fieldsets = (
        (None, {'fields': ('name',)}),
        ('Permissions', {'fields': ('permissions',)}),
    )

    def permissions_list(self, obj):
        return ", ".join([perm.codename for perm in obj.permissions.all()])
    permissions_list.short_description = 'Permissions'

class PermissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'codename')
    search_fields = ('codename',)
    ordering = ('codename',)
    fieldsets = (
    (None, {'fields': ('name', 'codename')}),
)


admin.site.register(Role, RoleAdmin)
admin.site.register(Permission, PermissionAdmin)