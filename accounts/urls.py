from django.urls import path
from .views import TestAPIView, RegisterUserView, LoginUserView, ListUserView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('test/<int:q>/', TestAPIView.as_view(), name='test-api'),
    path('users/', ListUserView.as_view(), name='list-users'),
]