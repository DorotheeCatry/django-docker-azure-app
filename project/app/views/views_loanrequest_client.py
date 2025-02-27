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

REQUEST_URL = ""

class LoanRequestView(FormView):
    """
    Class-based view for loan request.
    """
    template_name = "app/client-loanrequest.html"
    form_class = LoanRequestForm

    def form_valid(self, form):
        """
        This method is called when the form is valid.
        """
        # Create a LoanRequest instance without saving it immediately
        loan_request = form.save(commit=False)

        # Associate the current logged-in user to the loan request
        loan_request.user = self.request.user  # Using the logged-in user

        # Save the loan request to the database
        loan_request.save()

        # Optional: Send to an external API or additional action
        hist_response = requests.post(REQUEST_URL, json={
            "GrAppv": float(loan_request.amount),
            "Term": loan_request.term,
            "State": loan_request.state,
            "NAICS_Sectors": loan_request.naics,
            "New": loan_request.new,
            "Franchise": loan_request.franchise,
            "NoEmp": loan_request.no_emp,
            "RevLineCr": 0,
            "LowDoc": 0,
            "Rural": 0
        })

        if hist_response.status_code != 200:
            return JsonResponse({"error": "API Error"}, status=hist_response.status_code)

        if not hist_response.json():
            loan_request.status = "refused"
            loan_request.save()

        return render(self.request, self.template_name, {"form": form, "success": True})

    def form_invalid(self, form):
        """
        This method is called when the form is invalid.
        """
        # Display form errors in the template
        return render(self.request, self.template_name, {"form": form, "error": "There are errors in the form."})
    
@method_decorator(csrf_exempt, name='dispatch')  # Allows AJAX POST requests (ensure CSRF token in production)
class UpdatePredictionStatusView(View):
    """
    Updates the status of a loan request prediction.
    """

    def post(self, request, prediction_id):
        try:
            data = json.loads(request.body)
            new_status = data.get("status", "").lower()

            prediction = LoanRequest.objects.get(id=prediction_id)
            prediction.status = new_status
            prediction.save()

            return JsonResponse({"success": True})
        except LoanRequest.DoesNotExist:
            return JsonResponse({"error": "Prediction not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
        

class ClientLoanRequestView(ListView):
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
