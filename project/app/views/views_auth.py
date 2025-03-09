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
            user = User.objects.get(email=username)  # Replace username with email
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

class ClientLoginView(LoginView):
    """
    Login view for clients only.
    """
    authentication_form = AuthenticationForm
    
    def get_template_names(self):
        if self.request.user.is_authenticated:
            if self.request.user.role == 'client':
                return 'app/login-client.html'
            else:
                messages.error(self.request, "Unauthorized access. You are not a client.")
                return 'app/login.html'  # Error page
        return 'app/login-client.html'
    
    def get_success_url(self):
        return reverse('client-dashboard')
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.role != 'client':
                messages.error(request, "Unauthorized access. You must be a client.")
                return redirect('login')
            return redirect('client-dashboard')
        return super().dispatch(request, *args, **kwargs)

class AdvisorLoginView(LoginView):
    """
    Login view for advisors only.
    """
    authentication_form = AuthenticationForm
    
    def get_template_names(self):
        if self.request.user.is_authenticated:
            if self.request.user.role == 'advisor':
                return 'app/login-advisor.html'
            else:
                messages.error(self.request, "Unauthorized access. You are not an advisor.")
                return 'app/login.html'
        return 'app/login-advisor.html'
    
    def get_success_url(self):
        return reverse('advisor-dashboard')
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.role != 'advisor':
                messages.error(request, "Unauthorized access. You must be an advisor.")
                return redirect('login')
            return redirect('advisor-dashboard')
        return super().dispatch(request, *args, **kwargs)

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
    

