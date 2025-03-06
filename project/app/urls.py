from django.urls import path
from app.views.views_auth import UserLogoutView, SignupView, AdvisorLoginView, ClientLoginView
from app.views.views_pages import HomeView, ClientDashboardView, HomeLoginView
from app.views.views_loanrequest_client import loan_request_view, update_prediction_status, loan_predictions_view, submit_loan_request
from app.views.views_loanrequest_advisor import loan_predictions, AdvisorDashboardView, ClientDetailsView


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', HomeLoginView.as_view(), name='login'),
    path('login-client/', ClientLoginView.as_view(), name='login-client'),
    path('login-advisor/', AdvisorLoginView.as_view(), name='login-advisor'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('client-dashboard/', ClientDashboardView.as_view(), name='client-dashboard'),
    path('client-loanrequest/', loan_request_view, name='client-loanrequest'),
    path('advisor-dashboard/', AdvisorDashboardView.as_view(), name='advisor-dashboard'),
    path('advisor-loanrequest/', loan_predictions, name='advisor-loanrequest'),
    path("update_prediction/<int:prediction_id>/", update_prediction_status, name="update-prediction-status"),
    path("submit-loan/<int:loan_id>/", submit_loan_request, name="submit-loan"),
    path('client-loanstatus/', loan_predictions_view, name='client-loanstatus'),
    path('client/<int:id>/', ClientDetailsView.as_view(), name='client_details'),
]