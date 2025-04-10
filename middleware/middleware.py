from django.utils.deprecation import MiddlewareMixin
from django.urls import resolve
import jwt
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.conf import settings
from datetime import datetime
from .jwt_authentication import JWTAuthentication  # Assuming this is the correct import path

User = get_user_model()


class JWTAuthenticationMiddleware(MiddlewareMixin):
    """
    Middleware to handle JWT authentication for protected routes.
    """

    def process_request(self, request):
        # Skip middleware for admin, static, or media URLs
        if (
            request.path.startswith('/admin') or
            request.path.startswith('/static') or
            request.path.startswith('/media')
        ):
            return None  # No authentication check for admin or static/media paths

        # List of public route names (URLs with no JWT required)
        public_routes = ['login', 'register', 'websocket_test']

        try:
            # Resolve the URL path to get the route name
            resolver_match = resolve(request.path)
            route_name = resolver_match.url_name
        except:
            # If URL resolution fails, possibly skip this request
            return None

        # If the route is public, no authentication is required
        if route_name in public_routes:
            return None  # Allow access to public routes without authentication

        # Authenticate the request
        jwt_auth = JWTAuthentication()  # Initialize JWTAuthentication class
        user = jwt_auth.authenticate(request)  # Get user from token (or None if invalid)

        if user is None:
            # If no valid user is found in the token, return an error response
            return JsonResponse({"error": "Authentication credentials were not provided."}, status=401)

        # Attach the authenticated user to the request object
        request.user = user






