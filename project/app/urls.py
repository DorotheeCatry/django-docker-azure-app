from django.urls import path
from app.views.views_auth import UserLogoutView, SignupView, CustomLoginAdvisorView, CustomLoginClientView, loan_predictions, validations
from app.views.views_pages import HomeView, AdvisorDashboardView, ClientDashboardView, HomeLoginView
#from app.views.estimation import prediction
from app.views.views_loanrequest import loan_request_view, update_prediction_status, loan_predictions_view

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', HomeLoginView.as_view(), name='login'),
    path('login-client/', CustomLoginClientView.as_view(), name='login-client'),
    path('login-advisor/', CustomLoginAdvisorView.as_view(), name='login-advisor'),
    path('client-dashboard/', ClientDashboardView.as_view(), name='client-dashboard'),
    path('advisor-dashboard/', AdvisorDashboardView.as_view(), name='advisor-dashboard'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    #path('history/', loan_predictions, name='history'),
    path('validation/', validations, name='validation'),
    path("update_prediction/<int:prediction_id>/", update_prediction_status, name="update_prediction_status"),
    #path('prediction/', prediction, name='prediction'), 
    path('clienthistory/', loan_predictions_view, name='loansprediction'), 
    path('client-loanrequest/', loan_request_view, name = "loan-request"),

]