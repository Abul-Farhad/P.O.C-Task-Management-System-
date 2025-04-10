from django.http import JsonResponse
from django.urls import resolve
import jwt
from django.contrib.auth import get_user_model
User = get_user_model()
from django.conf import settings

class JWTAuthentication:
    """
    Custom JWT Authentication class for plain Django project.
    This can be used in views to manually authenticate users based on JWT tokens.
    """

    def authenticate(self, request):
        """
        Authenticate the user based on the Authorization header.
        """
        print("JWTAuthentication.authenticate called")

        # Get the Authorization header
        auth = request.headers.get('Authorization')

        if not auth:
            return None  # No auth token provided

        # Split the 'Authorization' header to extract the token
        parts = auth.split()

        if len(parts) != 2:
            return JsonResponse({"error": "Invalid Authorization header format"}, status=401)

        token = parts[1]

        try:
            # Decode the JWT token
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return JsonResponse({"error": "Token has expired"}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({"error": "Invalid token"}, status=401)

        # Get the user from the payload
        try:
            user = User.objects.get(id=payload['user_id'])
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=401)

        # Return the user object if the token is valid
        return user

