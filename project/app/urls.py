from django.urls import path
from project.app.views.views_auth import UserLogoutView, SignupView, CustomLoginAdvisorView, CustomLoginClientView
from project.app.views.views_pages import HomeView, AdvisorDashboardView, ClientDashboardView, HomeLoginView
#from app.views.estimation import estimation_history, prediction
from project.app.views.views_loanrequest import loan_request_view

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', HomeLoginView.as_view(), name='login'),
    path('login-client/', CustomLoginClientView.as_view(), name='login-client'),
    path('login-advisor/', CustomLoginAdvisorView.as_view(), name='login-advisor'),
    path('client-dashboard/', ClientDashboardView.as_view(), name='client-dashboard'),
    path('advisor-dashboard/', AdvisorDashboardView.as_view(), name='advisor-dashboard'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    #path('history/', estimation_history, name='history'),
    #path('prediction/', prediction, name='prediction'), 
    #path('client_loanstatus/', client_loanstatus, name='client_loanstatus'),
    path('client-loanrequest/', loan_request_view, name = "loan-request")
    #path('welcome/', WelcomeView.as_view(), name='welcome'),

    # For the users
    #path('profile/', UserProfileView.as_view(), name='profile'),
    #path('predict-charges/', PredictChargesView.as_view(), name='predict'),
    #path('prediction-history/', PredictionHistoryView.as_view(), name='prediction_history'),
    #path("book/", book_appointment, name="book_appointment"),
   
    #path('admin-appointments/', admin_appointment_list, name='admin_appointment_list'),

    # Other website pages
    #path('about/',AboutView.as_view(), name='about'),
    #path('join-us/', JoinUsView.as_view(), name='join_us'),
    #path('apply/', apply, name='apply'),
    #path('contact/', contact_view, name='contact'),
    #path('contact-us/', contact_view_user, name='contact_form'),
    #path('apply/', ApplyView.as_view(), name='apply'),
    #path('thank-you/', TemplateView.as_view(template_name='insurance_app/apply_thank_you.html'), name='apply_thank_you'), #thank you after applying a job
    #path('health-advices/', HealthAdvicesView.as_view(), name='health_advices'),
    #path('cybersecurity-awareness/',CybersecurityAwarenessView.as_view(), name='cybersecurity_awareness'),
    #path('messages/', message_list_view, name='messages_list'),
    #path('solve-message/<int:message_id>/', solve_message, name='solve_message'),
    #path('quote-predict/', predict_charges, name='predict_charges'),

    # Password (Change or Reset) URLs
    #path('password_reset/', auth_views.PasswordResetView.as_view(template_name='insurance_app/password_reset_form.html'), name='password_reset'),
    #path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='insurance_app/password_reset_done.html'), name='password_reset_done'),
    #path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='insurance_app/password_reset_confirm.html'), name='password_reset_confirm'),
    #path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='insurance_app/password_reset_complete.html'), name='password_reset_complete'),
    #path('changepassword/', ChangePasswordView.as_view(), name='changepassword'), # Change within profile 

    #administration
    #path('get-available-times/', get_available_times, name='get_available_times'),
    #path('testing/', TestingView.as_view(), name='testing')
]