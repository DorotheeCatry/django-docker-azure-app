from django.shortcuts import render, redirect
from django.http import JsonResponse
import requests
from app.forms import LoanRequestForm
from app.models import LoanRequest, UserProfile

REQUEST_URL="http://127.0.0.1:6000/loans/request"
def loan_request_view(request):
    if request.method == 'POST':
        form = LoanRequestForm(request.POST)
        if form.is_valid(): 
            loan_request = LoanRequest()
            loan_request.amount = form.cleaned_data['amount']
            loan_request.term = form.cleaned_data['term']
            loan_request.state = form.cleaned_data['state']
            loan_request.naics = form.cleaned_data['naics']
            loan_request.new = form.cleaned_data['new']
            loan_request.franchise = form.cleaned_data['franchise']
            loan_request.no_emp = form.cleaned_data['no_emp']
            loan_request.user = UserProfile(id=1)
            loan_request.save()
            hist_response = requests.post(REQUEST_URL, json={"GrAppv": float(loan_request.amount),"Term": loan_request.term,
                                                             "State": loan_request.state,"NAICS_Sectors": loan_request.naics,
                                                             "New": loan_request.new,"Franchise": loan_request.franchise,
                                                             "NoEmp" : loan_request.no_emp,"RevLineCr": 0,
                                                             "LowDoc": 0,"Rural": 0 })
            print("Hist Response JSON:", hist_response.json())
            if hist_response.status_code != 200:
                return JsonResponse({"error": "Erreur API"}, status=hist_response.status_code)
            if not hist_response.json():
                loan_request.status = "refused"
                loan_request.save()
            return render(request, "app/client_loanrequest.html", {"form": form}) 
    else:
        form = LoanRequestForm()  # Création d'un formulaire vide pour un GET
    return render(request, "app/client_loanrequest.html", {"form": form})

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt  # Allows AJAX POST requests (ensure CSRF token in production)
def update_prediction_status(request, prediction_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            new_status = data.get("status").lower()

            prediction = LoanRequest.objects.get(id=prediction_id)
            prediction.status = new_status
            prediction.save()

            return JsonResponse({"success": True})
        except LoanRequest.DoesNotExist:
            return JsonResponse({"error": "Prediction not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
