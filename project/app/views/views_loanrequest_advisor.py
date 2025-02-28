from django.shortcuts import render
from app.forms import LoanRequestForm
from django.views.generic.edit import FormView
from django.views.generic import ListView
from django.http import JsonResponse
import requests
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
from app.models import LoanRequest
from django.contrib.auth.decorators import login_required


class AdvisorLoanRequestView(ListView):
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
    
@login_required
def loan_predictions(request):
    predictions = LoanRequest.objects.all()  # Fetch all loan requests
    return render(request, "app/advisor-loan-predictions.html", {"predictions": predictions})