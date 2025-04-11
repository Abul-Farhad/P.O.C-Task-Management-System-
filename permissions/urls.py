from django.urls import path
from .views import (
    CreateRoleView, AssignRoleView, 
    UpdateRoleView, DeleteRoleView, 
    ListRoleView, DeleteUserRoleView,
    ListPermissionView)

urlpatterns = [
    path('create-role/', CreateRoleView.as_view(), name='create-role'),
    path('assign-role/', AssignRoleView.as_view(), name='assign-role'),
    path('update-role/', UpdateRoleView.as_view(), name='update-role'),
    path('delete-role/', DeleteRoleView.as_view(), name='delete-role'),
    path('delete-user-role/', DeleteUserRoleView.as_view(), name='delete-user-role'),
    path('list-role/', ListRoleView.as_view(), name='list-role'),
    path('list-permission/', ListPermissionView.as_view(), name='list-permission'),
]