from django.urls import path
from app.views.auth import HomeView, CustomLoginView, UserLogoutView, SignupView, loan_predictions, validations
from app.views.auth import HomeView, prediction, login

from app.views.base import loan_request_view

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout_user'),
    path('login-api/', login, name='login'),
    path('history/', loan_predictions, name='history'),
    path('validation/', validations, name='validation'),
    path('prediction/', prediction, name='prediction'), 
    path('client_loanrequest/', loan_request_view, name = "loan_request")
]