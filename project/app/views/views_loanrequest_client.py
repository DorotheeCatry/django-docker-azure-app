from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
import requests
from app.forms import LoanRequestForm
from app.models import LoanRequest
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.decorators import login_required
from app.utils.api_connect import get_api_token
import os
from dotenv import load_dotenv


load_dotenv()

API_LOANREQUEST_URL = os.getenv("API_LOANREQUEST_URL")
API_USER_ID = os.getenv("API_USER_ID")

@login_required
def loan_request_view(request):
    if request.method == "POST":
        form = LoanRequestForm(request.POST)
        
        if form.is_valid():
            user_profile = request.user

            # Création de l'objet LoanRequest en base de données
            loan_request = LoanRequest()
            loan_request.amount = form.cleaned_data['amount']
            loan_request.term = form.cleaned_data['term']
            loan_request.state = form.cleaned_data['state']
            loan_request.naics = form.cleaned_data['naics']
            loan_request.new = form.cleaned_data['new']
            loan_request.franchise = form.cleaned_data['franchise']
            loan_request.no_emp = form.cleaned_data['no_emp']
            loan_request.rev_line_cr = form.cleaned_data['rev_line_cr']
            loan_request.low_doc = form.cleaned_data['low_doc']
            loan_request.rural = form.cleaned_data['rural']
            loan_request.user = user_profile
            loan_request.advisor = user_profile.advisor
            loan_request.save()

            # Récupérer le token API et l'user_id
            token = get_api_token()
            
            # Préparer les en-têtes pour l'API FastAPI
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            
            data = {
                "GrAppv": float(loan_request.amount),
                "Term": loan_request.term,
                "State": loan_request.state,
                "NAICS_Sectors": loan_request.naics,
                "New": loan_request.new,
                "Franchise": loan_request.franchise,
                "NoEmp": loan_request.no_emp,
                "RevLineCr": loan_request.rev_line_cr,
                "LowDoc": loan_request.low_doc,
                "Rural": loan_request.rural
            }

            # Envoi de la requête à l'API FastAPI
            hist_response = requests.post(API_LOANREQUEST_URL, json=data, headers=headers)

            # Debug print statements
            print(headers)
            print(data)
            print("Hist Response JSON:", hist_response.json())

            # Vérifier la réponse de l'API
            if hist_response.status_code != 200:
                return JsonResponse({"error": "Erreur API"}, status=hist_response.status_code)

            # Mise à jour du statut du prêt
            api_response = hist_response.json()
            if not api_response:
                loan_request.status = "refused"
            elif hist_response.status_code == 200:
                loan_request.status = "pending"

            loan_request.save()

            return JsonResponse({"message": "Loan request processed", "status": loan_request.status})

        else:
            # En cas d'erreur dans le formulaire
            print("form errors", form.errors.as_json())
            return render(request, "app/client-loanrequest.html", {"form": form}) 
    else:
        # Création d'un formulaire vide pour une requête GET
        form = LoanRequestForm()
    return render(request, "app/client-loanrequest.html", {"form": form})

        
def submit_loan_request(request, loan_id):
    """
    Envoie une demande de prêt spécifique à l'API FastAPI
    """
    loan_request = get_object_or_404(LoanRequest, id=loan_id)

    try:
        response = loan_request.send_to_api()
        return JsonResponse(response, safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


@login_required
def loan_predictions_view(request):
    # Filter predictions for user_id == 1
    print("Utilisateur connecté :", request.user)  # Debug
    user = request.user
    predictions = LoanRequest.objects.filter(user=user)

    # Pass filtered predictions to the template
    return render(request, "app/client-loanstatus.html", {"predictions": predictions})
