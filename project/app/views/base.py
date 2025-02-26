from django.shortcuts import render, redirect
from app.forms import LoanRequestForm

REQUEST_URL="127....600/loans/history"
def loan_request_view(request):
    if request.method == 'POST':
        form = LoanRequestForm(request.POST) 
        if form.is_valid():  
            form.save()
            hist_response = requests.post(REQUEST_URL, json={"id": 0,"GrAppv": 18000,"Term": 1,"State": "CA","NAICS_Sectors": 54000,"New": 0,"Franchise": 0,"NoEmp" : 0,"RevLineCr": 0,"LowDoc": 0,"Rural": 0 })
            print("Hist Response Status:", hist_response.status_code)
            print("Hist Response JSON:", hist_response.json())
            if hist_response.status_code != 200:
                return JsonResponse({"error": "Erreur API"}, status=hist_response.status_code)
            return redirect('#page redirection??')  
    else:
        form = LoanRequestForm()  # Création d'un formulaire vide pour un GET
    return render(request, "app/client_loanrequest.html", {"form": form})

