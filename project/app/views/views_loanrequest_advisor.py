from django.views.generic import TemplateView, DetailView
from app.models import LoanRequest, UserProfile
from django.db.models import Sum, Avg, Count, F, ExpressionWrapper, fields
from django.shortcuts import get_object_or_404
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
from django.db.models.functions import ExtractDay

# Page 1 - Advisor Dashboard
class AdvisorDashboardView(TemplateView):
    template_name = 'app/advisor-dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        advisor_profile = self.request.user
        now = datetime.now()
        month_ago = now - timedelta(days=30)

        # Base queryset for loan requests
        loan_requests = LoanRequest.objects.filter(advisor=advisor_profile)
        
        # Current month and previous month loans
        current_month_loans = loan_requests.filter(created_at__month=now.month)
        previous_month_loans = loan_requests.filter(created_at__month=(now.month-1 if now.month > 1 else 12))

        # Calculate loan growth
        current_month_total = current_month_loans.aggregate(total=Sum('amount'))['total'] or 0
        previous_month_total = previous_month_loans.aggregate(total=Sum('amount'))['total'] or 1  # Avoid division by zero
        loan_growth = ((current_month_total - previous_month_total) / previous_month_total) * 100

        # Basic statistics
        total_loaned = loan_requests.aggregate(total=Sum('amount'))['total'] or 0
        avg_loan = loan_requests.aggregate(avg=Avg('amount'))['avg'] or 0
        total_loans = loan_requests.count()
        approved_count = loan_requests.filter(status='approved').count()
        pending_count = loan_requests.filter(status='pending').count()
        rejected_count = loan_requests.filter(status='rejected').count()
        approval_rate = round((approved_count / total_loans * 100)) if total_loans else 0

        # Client statistics
        active_clients = loan_requests.values('user').distinct().count()
        new_clients = loan_requests.filter(
            created_at__gte=month_ago
        ).values('user').distinct().count()

        # Loan trend data
        loan_data = loan_requests.values('created_at__date').annotate(
            total=Sum('amount')
        ).order_by('created_at__date')
        
        loan_dates = [entry['created_at__date'].strftime("%Y-%m-%d") for entry in loan_data]
        loan_amounts = [float(entry['total']) if entry['total'] else 0 for entry in loan_data]

        context.update({
            'now': now,
            'total_loaned': int(total_loaned),
            'avg_loan': int(avg_loan),
            'total_loans': total_loans,
            'loan_growth': loan_growth,
            'approval_rate': approval_rate,
            'approved_count': approved_count,
            'pending_count': pending_count,
            'rejected_count': rejected_count,
            'active_clients_count': active_clients,
            'new_clients_count': new_clients,
            'loan_dates': json.dumps(loan_dates),
            'loan_amounts': json.dumps(loan_amounts),
            'recent_loans': loan_requests.select_related('user').order_by('-created_at')[:10]
        })

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

# Page 2 - Advisor Loan Requests
class AdvisorLoanRequestView(TemplateView):
    """
    Displays loan predictions for the authenticated user.
    """
    model = LoanRequest
    template_name = "app/advisor-loanrequest.html"

    def get_context_data(self, **kwargs):
        """
        Adds the loan requests to the template context under the key 'loans'.
        """
        context = super().get_context_data(**kwargs)

        # Get advisor profile
        advisor_profile = self.request.user

        # Get clients for this advisor
        clients = UserProfile.objects.filter(advisor_id=advisor_profile.id)
        context['clients'] = clients

        # Get all loan requests for this advisor
        loans = LoanRequest.objects.filter(advisor_id=advisor_profile.id)
        context['loans'] = loans

        # Global statistics
        loan_requests = LoanRequest.objects.filter(advisor_id=advisor_profile.id)
        total_loaned = loan_requests.aggregate(total_amount=Sum('amount'))['total_amount'] or Decimal(0)
        avg_loan = loan_requests.aggregate(average_amount=Avg('amount'))['average_amount'] or Decimal(0)
        total_count = loan_requests.count()
        approved_count = loan_requests.filter(status='approved').count()
        approval_rate = round((approved_count / total_count * 100)) if total_count else 0

        # Convert Decimal to int
        context['total_loaned'] = int(total_loaned)
        context['avg_loan'] = int(avg_loan)
        context['approval_rate'] = approval_rate

        # Loan data for charts (loan amounts by date)
        loan_data = loan_requests.values('created_at').annotate(total=Sum('amount')).order_by('created_at')
        loan_dates = [entry['created_at'].strftime("%Y-%m-%d") for entry in loan_data]
        loan_amounts = [int(entry['total']) if entry['total'] else 0 for entry in loan_data]

        # Pass data in JSON format
        context['loan_dates'] = json.dumps(loan_dates)
        context['loan_amounts'] = json.dumps(loan_amounts)

        return context


# Update the loan request status, only done by the proper advisor
@csrf_exempt  # Allows AJAX POST requests (ensure CSRF token in production)
def update_loan_status(request, loan_id):
    """
    Updates the status of a loan request.
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            new_status = data.get("status").lower()

            loan = LoanRequest.objects.get(id=loan_id)
            loan.status = new_status
            loan.save()

            return JsonResponse({"success": True})
        except LoanRequest.DoesNotExist:
            return JsonResponse({"error": "Loan not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
