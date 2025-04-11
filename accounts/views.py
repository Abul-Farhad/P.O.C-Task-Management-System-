from django.http import JsonResponse
from django.views import View
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .forms import UserRegistrationForm, UserLoginForm
import jwt, datetime, os, json
from django.conf import settings
from accounts.models import CustomUser

SECRET_KEY = os.getenv('JWT_SECRET_KEY')

@method_decorator(csrf_exempt, name='dispatch')  # Disable CSRF for simplicity (not recommended for production)
class RegisterUserView(View):
    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        form = UserRegistrationForm(data=data)
        if form.is_valid():
            email = form.cleaned_data["email"]

            if CustomUser.objects.filter(email=email).exists():
                return JsonResponse({"error": "User already exists!"}, status=400)

            form.save()  # Save the user to the database
            return JsonResponse({"message": "User created successfully!", "data": form.cleaned_data}, status=201)
        else:
            return JsonResponse({"error": form.errors}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class LoginUserView(View):
    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        print(data)
        form = UserLoginForm(data=data)

        if form.is_valid():
            print("Form is valid")
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            try:
                user = CustomUser.objects.get(email=email)
                if not user.check_password(password):
                    return JsonResponse({"error": "Invalid credentials!"}, status=401)

                payload = {
                    'user_id': user.id,
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
                    'iat': datetime.datetime.utcnow()
                }
                token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm='HS256')

                return JsonResponse({
                    'message': 'Login successful!',
                    'token': token
                }, status=200)

            except CustomUser.DoesNotExist:
                return JsonResponse({"error": "User does not exist!"}, status=404)
        else:
            return JsonResponse({"error": form.errors}, status=400)
        

@method_decorator(csrf_exempt, name='dispatch')
class TestAPIView(View):
    def get(self, request, *args, **kwargs):
        print(request.GET)
        print(kwargs)
        return JsonResponse({"message": "This is a test API view!"}, status=200)

@method_decorator(csrf_exempt, name='dispatch')
class ListUserView(View):
    def get(self, request):
        users = CustomUser.objects.all().order_by('id')
        user_list = [{"id": user.id, "email": user.email, "role": "Not Assigned" if user.role is None else user.role.name} for user in users]
        return JsonResponse({"users": user_list}, status=200)