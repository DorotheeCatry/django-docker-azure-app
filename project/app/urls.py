from django.urls import path
from app.views.views_auth import UserLogoutView, SignupView, AdvisorLoginView, ClientLoginView
from app.views.views_pages import HomeView, ClientDashboardView, HomeLoginView, ContactView, AboutView, ServicesView
from app.views.views_loanrequest_client import loan_request_view, loan_predictions_view, submit_loan_request
from app.views.views_loanrequest_advisor import AdvisorDashboardView, ClientDetailsView, AdvisorLoanRequestView, update_loan_status


urlpatterns = [
    # Home
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='home-about'),
    path('services/', ServicesView.as_view(), name='home-services'),
    path('contact/', ContactView.as_view(), name='home-contact'),
    # Login
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', HomeLoginView.as_view(), name='login'),
    path('login-client/', ClientLoginView.as_view(), name='login-client'),
    path('login-advisor/', AdvisorLoginView.as_view(), name='login-advisor'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    # Client board
    path('client-dashboard/', ClientDashboardView.as_view(), name='client-dashboard'),
    path('client-loanrequest/', loan_request_view, name='client-loanrequest'),
    # Advisor Board
    path('advisor-dashboard/', AdvisorDashboardView.as_view(), name='advisor-dashboard'),
    path('advisor-loanrequest/', AdvisorLoanRequestView.as_view(), name='advisor-loanrequest'),
    path("update_loan_status/<int:loan_id>/", update_loan_status, name="update_loan_status"),
    path("submit-loan/<int:loan_id>/", submit_loan_request, name="submit-loan"),
    path('client-loanstatus/', loan_predictions_view, name='client-loanstatus'),
    path('client/<int:id>/', ClientDetailsView.as_view(), name='client_details'),
]