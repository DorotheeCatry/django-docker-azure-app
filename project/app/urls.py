from django.urls import path
from app.views.views_auth import UserLogoutView, SignupView, CustomLoginAdvisorView, CustomLoginClientView
from app.views.views_pages import HomeView, AdvisorDashboardView, ClientDashboardView, HomeLoginView
from app.views.views_loanrequest_client import loan_request_view, update_prediction_status, loan_predictions_view
from app.views.views_loanrequest_advisor import loan_predictions


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', HomeLoginView.as_view(), name='login'),
    path('login-client/', CustomLoginClientView.as_view(), name='login-client'),
    path('login-advisor/', CustomLoginAdvisorView.as_view(), name='login-advisor'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('client-dashboard/', ClientDashboardView.as_view(), name='client-dashboard'),
    path('client-loanrequest/', loan_request_view, name='client-loanrequest'),
    path('advisor-dashboard/', AdvisorDashboardView.as_view(), name='advisor-dashboard'),
    path('advisor-loanrequest/', loan_predictions, name='advisor-loanrequest'),
    path("update_prediction/<int:prediction_id>/", update_prediction_status, name="update-prediction-status"),
    path('client-loanstatus/', loan_predictions_view, name='client-loanstatus'),
]