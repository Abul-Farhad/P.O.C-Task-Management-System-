from django.urls import path
from .views import CreateRoleView, AssignRoleView, UpdateRoleView, DeleteRoleView

urlpatterns = [
    path('create-role/', CreateRoleView.as_view(), name='create-role'),
    path('assign-role/', AssignRoleView.as_view(), name='assign-role'),
    path('update-role/', UpdateRoleView.as_view(), name='update-role'),
    path('delete-role/', DeleteRoleView.as_view(), name='delete-role'),
]