from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth import logout
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from app.forms import UserSignupForm, ChangePasswordForm, AuthenticationForm
from app.models import UserProfile
from django.views.generic.edit import CreateView
import requests
from django.http import JsonResponse
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from app.models.model_loanrequest import LoanRequest
import os
from dotenv import load_dotenv, set_key

ENV_FILE = ".env"
load_dotenv()
AUTH_URL = os.getenv("AUTH_URL")

User = get_user_model()

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(email=username)  # Remplace username par email
        except User.DoesNotExist:
            return None
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None

class SignupView(CreateView):
    """
    Handles user sign-up.
    """
    model = UserProfile
    form_class = UserSignupForm
    template_name = 'app/signup.html'
    success_url = reverse_lazy('login')

class CustomLoginClientView(LoginView):
    """
    Custom login view for clients with 'remember me' functionality.
    """
    authentication_form = AuthenticationForm
    template_name = 'app/login-client.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse('client-dashboard')

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('client-dashboard')
        return super().dispatch(request, *args, **kwargs)
    
    def connect_to_api(self):
        if self.request.user.is_authenticated:
            print("hi")
            username = os.getenv("API_USERNAME")
            password = os.getenv("API_PASSWORD")
        
            if not username or password:
                raise Exception("NO")
            
            login_data = {
                "username": username,
                "password": password
            }
            
            response = requests.post(AUTH_URL, json=login_data)
            if response.status_code == 200:
                token = response.json()["access_token"]
                set_key(ENV_FILE, "API_TOKEN", token)
                
                print(token)
                return token
            else:
                raise Exception("Failed to login at the API")

class CustomLoginAdvisorView(LoginView):
    """
    Custom login view for advisors with 'remember me' functionality.
    """
    authentication_form = AuthenticationForm
    template_name = 'app/login-advisor.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse('advisor-dashboard')
    
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('advisor-dashboard')
        return super().dispatch(request, *args, **kwargs)


class ChangePasswordView(PasswordChangeView):
    """
    Handles password change requests.
    """
    form_class = ChangePasswordForm
    template_name = 'app/changepassword.html'
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Your password has been changed successfully!')
        return response

class UserLogoutView(LoginRequiredMixin, View):
    """
    Handles user logout requests.
    """
    template_name = 'app/logout.html'

    def get(self, request):
        user = self.request.user
        return render(request, self.template_name, {'user': user})

    def post(self, request):
        logout(request)
        return render(request, self.template_name, {'user': None})
    

def login(request):

    auth_response = requests.post(AUTH_URL, params={"email": "d", "password": "davdorothee@advisor.frid"})
    print("Hist Response Status:", auth_response.status_code)
    print("Hist Response JSON:", auth_response.json()) 
    if auth_response.status_code != 200:
        return JsonResponse({"error": "Échec de l'authentification"}, status=auth_response.status_code)
    
    token = auth_response.json().get("access_token")  # Extract token

    if not token:
        return JsonResponse({"error": "Token non reçu"}, status=401)
    
    return render(request, 'app/test.html')

