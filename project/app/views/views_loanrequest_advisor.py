from django.shortcuts import render
from django.views.generic import ListView, TemplateView, DetailView
from app.models import LoanRequest, UserProfile
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Avg
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
import json
from decimal import Decimal



class AdvisorLoanRequestView(ListView):
    """
    Displays loan predictions for the authenticated user.
    """
    model = LoanRequest
    template_name = "app/advisor-loanrequest.html"

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
        
        advisor_profile = self.request.user
        if not hasattr(advisor_profile, 'role') or advisor_profile.role != 'advisor':
            raise PermissionDenied("You must be an advisor to access this page.")

        # Récupérer les clients de cet advisor
        clients = UserProfile.objects.filter(advisor_id=advisor_profile.id)
        context['clients'] = clients

        # Récupérer les demandes de prêt en attente
        predictions = LoanRequest.objects.filter(advisor=advisor_profile, status='pending')
        context['predictions'] = predictions
        # Statistiques globales sur les prêts
        loan_requests = LoanRequest.objects.filter(advisor=advisor_profile)
        total_loaned = round(loan_requests.aggregate(total_amount=Sum('amount'))['total_amount']) or Decimal(0)
        avg_loan = round(loan_requests.aggregate(average_amount=Avg('amount'))['average_amount']) or Decimal(0)
        total_count = loan_requests.count()
        approved_count = loan_requests.filter(status='approved').count()
        approval_rate = round((approved_count / total_count * 100)) if total_count else 0

        # Convertir Decimal en float
        context['total_loaned'] = int(total_loaned)
        context['avg_loan'] = int(avg_loan)
        context['approval_rate'] = int(approval_rate)

        # Données pour le graphique (montants prêtés par date)
        loan_data = loan_requests.values('created_at__date').annotate(total=Sum('amount')).order_by('created_at__date')
        loan_dates = [entry['created_at__date'].strftime("%Y-%m-%d") for entry in loan_data]
        loan_amounts = [int(entry['total']) if entry['total'] else 0 for entry in loan_data]

        # Passer les données en JSON
        context['loan_dates'] = json.dumps(loan_dates)
        context['loan_amounts'] = json.dumps(loan_amounts)

        # Debugging
        print("Loan Dates:", context['loan_dates'])
        print("Loan Amounts:", context['loan_amounts'])

        return context
    
@login_required
def loan_predictions(request):
    predictions = LoanRequest.objects.all()  # Fetch all loan requests
    return render(request, "app/advisor-loanrequest.html", {"predictions": predictions})



class AdvisorDashboardView(TemplateView):
    template_name = 'app/advisor-dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Vérifier que l'utilisateur est bien un conseiller
        advisor_profile = self.request.user
        if not hasattr(advisor_profile, 'role') or advisor_profile.role != 'advisor':
            raise PermissionDenied("You must be an advisor to access this page.")

        # Récupérer les clients de cet advisor
        clients = UserProfile.objects.filter(advisor_id=advisor_profile.id)
        context['clients'] = clients

        # Récupérer les demandes de prêt en attente
        predictions = LoanRequest.objects.filter(advisor=advisor_profile, status='pending')
        context['predictions'] = predictions
        # Statistiques globales sur les prêts
        loan_requests = LoanRequest.objects.filter(advisor=advisor_profile)
        total_loaned = round(loan_requests.aggregate(total_amount=Sum('amount'))['total_amount']) or Decimal(0)
        avg_loan = round(loan_requests.aggregate(average_amount=Avg('amount'))['average_amount']) or Decimal(0)
        total_count = loan_requests.count()
        approved_count = loan_requests.filter(status='approved').count()
        approval_rate = round((approved_count / total_count * 100)) if total_count else 0

        # Convertir Decimal en float
        context['total_loaned'] = int(total_loaned)
        context['avg_loan'] = int(avg_loan)
        context['approval_rate'] = int(approval_rate)

        # Données pour le graphique (montants prêtés par date)
        loan_data = loan_requests.values('created_at__date').annotate(total=Sum('amount')).order_by('created_at__date')
        loan_dates = [entry['created_at__date'].strftime("%Y-%m-%d") for entry in loan_data]
        loan_amounts = [int(entry['total']) if entry['total'] else 0 for entry in loan_data]

        # Passer les données en JSON
        context['loan_dates'] = json.dumps(loan_dates)
        context['loan_amounts'] = json.dumps(loan_amounts)

        # Debugging
        print("Loan Dates:", context['loan_dates'])
        print("Loan Amounts:", context['loan_amounts'])

        return context


class ClientDetailsView(DetailView):
    model = UserProfile
    template_name = 'app/client_details.html'
    context_object_name = 'client'

    def get_object(self):
        client_id = self.kwargs['id']
        return get_object_or_404(UserProfile, id=client_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Récupérer le client actuellement consulté
        client = self.get_object()

        # Récupérer toutes les demandes de prêts associées à ce client via 'user'
        loan_requests = LoanRequest.objects.filter(user=client)

        # Ajouter ces informations au contexte
        context['loan_requests'] = loan_requests

        # Retourner le contexte avec les informations supplémentaires
        return context