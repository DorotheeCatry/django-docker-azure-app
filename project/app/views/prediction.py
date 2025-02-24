from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.views.generic import ListView
from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse_lazy
from .models import PredictionHistory
from .forms import PredictChargesForm
import os
import pickle
import pandas as pd
from django.conf import settings
from django.db.models import Avg

class PredictChargesView(LoginRequiredMixin, UpdateView):
    """
    Handles insurance charge predictions.
    """
    model = PredictionHistory
    form_class = PredictChargesForm
    template_name = 'insurance_app/predict.html'
    success_url = reverse_lazy('predict')

    # (Code de la view PredictChargesView ici)

class PredictionHistoryView(LoginRequiredMixin, ListView):
    """
    Displays prediction history for the user.
    """
    model = PredictionHistory
    template_name = 'insurance_app/prediction_history.html'
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