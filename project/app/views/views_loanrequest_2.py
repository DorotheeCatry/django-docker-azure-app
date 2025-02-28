from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from app.models import LoanRequest


class ClientLoanRequestView(ListView, LoginRequiredMixin):
    """
    Displays loan predictions for the authenticated user.
    """
    model = LoanRequest
    template_name = "app/client-loanstatus.html"

    def get_queryset(self):
        """
        Filters the loan predictions to show only those of the currently logged-in user.
        """
        return LoanRequest.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        """
        Adds the loan requests to the template context under the key 'loans'.
        """
        context = super().get_context_data(**kwargs)
        context['loans'] = context['object_list']  # Renomme 'object_list' en 'loans'
        return context
