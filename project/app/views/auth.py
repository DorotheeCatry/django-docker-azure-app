from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth import logout
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from app.forms import UserSignupForm, ChangePasswordForm
from app.models import UserProfile
from django.views.generic.edit import CreateView
from django.views.generic import TemplateView

class HomeView(TemplateView):
    """
    Renders the homepage.

    This view is responsible for rendering the 'home.html' template, which serves as the 
    homepage for the application.

    Attributes:
        template_name (str): The name of the template used to display the response.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders the 'home.html' template.
    """
    template_name = 'app/home.html'  # Home Page View Template


class SignupView(CreateView):
    """
    Handles user sign-up.
    """
    model = UserProfile
    form_class = UserSignupForm
    template_name = 'app/signup.html'
    success_url = reverse_lazy('login')

class CustomLoginView(LoginView):
    """
    Custom login view with 'remember me' functionality.
    """
    template_name = 'app/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('welcome')

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('profile')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        remember_me = self.request.POST.get('remember_me', None) is not None
        if not remember_me:
            self.request.session.set_expiry(0)
        else:
            self.request.session.set_expiry(1209600)
        return super().form_valid(form)

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
    template_name = 'app/logout_user.html'

    def get(self, request):
        user = self.request.user
        return render(request, self.template_name, {'user': user})

    def post(self, request):
        logout(request)
        return render(request, self.template_name, {'user': None})