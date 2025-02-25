from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.views.generic import ListView
from django.urls import reverse_lazy
from app.models import PredictionHistory
from app.forms.client_loanrequest import PredictChargesForm
from django.db.models import Avg

class PredictLoanAcceptance(LoginRequiredMixin, UpdateView):
    """
    Handles insurance charge predictions.
    """
    model = PredictionHistory
    form_class = PredictChargesForm
    template_name = 'app/predict.html'
    success_url = reverse_lazy('predict')

    # (Code de la view PredictChargesView ici)

class PredictionHistoryView(LoginRequiredMixin, ListView):
    """
    Displays prediction history for the user.
    """
    model = PredictionHistory
    template_name = 'app/prediction_history.html'
    context_object_name = 'predictions'
    paginate_by = 10

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user).order_by('-timestamp')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'total_predictions': self.get_queryset().count(),
            'average_charges': self.get_queryset().aggregate(Avg('predicted_charges'))['predicted_charges__avg']
        })
        return context