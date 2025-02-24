from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.contrib import messages
from django.urls import reverse_lazy
from .forms import UserProfileForm
from django.contrib.auth import get_user_model

class UserProfileView(LoginRequiredMixin, UpdateView):
    """
    Handles user profile updates.
    """
    model = get_user_model()
    form_class = UserProfileForm
    template_name = 'insurance_app/profile.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Your profile has been updated!')
        return response