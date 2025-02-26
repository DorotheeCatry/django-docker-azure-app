from django.shortcuts import render, redirect
from app.forms import LoanRequestForm


def loan_request_view(request):
    if request.method == 'POST':
        form = LoanRequestForm(request.POST) 
        if form.is_valid():  
            form.save()  
            return redirect('#page redirection??')  
    else:
        form = LoanRequestForm()  # Création d'un formulaire vide pour un GET
    return render(request, "client_loanrequest.html", {"form": form})

