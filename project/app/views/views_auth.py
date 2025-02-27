from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth import logout
from django.urls import reverse_lazy
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

HIST_URL = "http://127.0.0.1:6000/loans/history"
REQUEST_URL = "http://127.0.0.1:6000/loans/request"


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
    success_url = reverse_lazy('client-dashboard')
    
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('client-dashboard')
        return super().dispatch(request, *args, **kwargs)

class CustomLoginAdvisorView(LoginView):
    """
    Custom login view for advisors with 'remember me' functionality.
    """
    authentication_form = AuthenticationForm
    template_name = 'app/login-advisor.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('advisor-dashboard')
    
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
    


def estimation_history(request):
    hist_response = requests.get(HIST_URL, params={"id": 0})
    print("Hist Response Status:", hist_response.status_code)
    print("Hist Response JSON:", hist_response.json())  # Check actual response
    if hist_response.status_code != 200:
        return JsonResponse({"error": "Erreur API"}, status=hist_response.status_code)
    return render(request, 'app/test.html')


def prediction(request):
    hist_response = requests.post(REQUEST_URL, json={"id": 0,"GrAppv": 18000,"Term": 1,"State": "CA","NAICS_Sectors": 54000,"New": 0,"Franchise": 0,"NoEmp" : 0,"RevLineCr": 0,"LowDoc": 0,"Rural": 0 })
    print("Hist Response Status:", hist_response.status_code)
    print("Hist Response JSON:", hist_response.json())
    if hist_response.status_code != 200:
        return JsonResponse({"error": "Erreur API"}, status=hist_response.status_code)
    return render(request, 'app/test.html')