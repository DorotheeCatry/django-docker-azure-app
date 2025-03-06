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
                messages.error(self.request, "Accès non autorisé. Vous n'êtes pas un client.")
                return 'app/error-page.html'  # Page d'erreur
        return 'app/login-client.html'
    
    def get_success_url(self):
        return reverse('client-dashboard')
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.role != 'client':
                messages.error(request, "Accès non autorisé. Vous devez être un client.")
                return redirect('error-page')
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
                messages.error(self.request, "Accès non autorisé. Vous n'êtes pas un conseiller.")
                return 'app/error-page.html'
        return 'app/login-advisor.html'
    
    def get_success_url(self):
        return reverse('advisor-dashboard')
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.role != 'advisor':
                messages.error(request, "Accès non autorisé. Vous devez être un conseiller.")
                return redirect('error-page')  # Redirection vers une page d'erreur
            return redirect('advisor-dashboard')  # Rediriger vers le tableau de bord si déjà connecté
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

