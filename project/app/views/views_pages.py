from django.views.generic import TemplateView, View
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from app.forms.form_contact import ContactForm
from django.shortcuts import render



class HomeView(TemplateView):
    """
    Renders the homepage.

    This view is responsible for rendering the 'home.html' template, which serves as the 
    homepage for the application.

    Attributes:
        template_name (str): The name of the template used to display the response.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders the 'home.html' template.
    """
    template_name = 'app/home.html'  # Home Page View Template
    
    
    
class HomeLoginView(TemplateView):
    """
    Renders the login homepage.

    This view is responsible for rendering the 'login.html' template, which serves as the 
    login homepage for the application. It redirects advisors or clients to their respective dashboards.

    Attributes:
        template_name (str): The name of the template used to display the response.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders the 'home-login.html' template.
    """
    template_name = 'app/login.html'  # Home Page View Template
    
    
class ClientDashboardView(TemplateView):
    """
    Renders the client dashboard.

    This view is responsible for rendering the 'client_dashboard.html' template, which serves as the 
    dashboard for the clients.

    Attributes:
        template_name (str): The name of the template used to display the response.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders the 'client_dashboard.html' template.
    """
    template_name = 'app/client-dashboard.html'
        


class ContactView(FormView):
    template_name = 'app/home-contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('app/home-contact')  # URL de redirection après soumission réussie

    def form_valid(self, form):
        # Logique d'envoi de l'email ou autre action après soumission du formulaire
        # Vous pouvez envoyer un email ici ou enregistrer les données dans la base de données
        # Exemple :
        # send_mail(
        #     'New Contact Form Submission',
        #     form.cleaned_data['message'],
        #     form.cleaned_data['email'],
        #     ['support@eliteloans.com'],
        # )
        return super().form_valid(form)
    
    
from django.shortcuts import render
from django.views import View

class ServicesView(View):
    def get(self, request):
        services = [
            {
                'icon': 'building',  # Icône pour les bâtiments commerciaux
                'title': "Commercial Real Estate",
                'description': "Finance your commercial property purchases with competitive rates and flexible terms tailored to your needs."
            },
            {
                'icon': 'briefcase',  # Icône pour les affaires
                'title': "Business Expansion",
                'description': "Get the capital you need to grow your business, hire new employees, or expand to new locations."
            },
            {
                'icon': 'chart-line',  # Icône pour la ligne de graphique (finance)
                'title': "Equipment Financing",
                'description': "Modernize your operations with new equipment financing solutions that keep you competitive."
            },
            {
                'icon': 'piggy-bank',  # Icône pour la tirelire
                'title': "Working Capital",
                'description': "Access flexible working capital to manage cash flow, inventory, and day-to-day operations."
            },
            {
                'icon': 'calculator',  # Icône pour la calculatrice
                'title': "Debt Consolidation",
                'description': "Streamline your finances by consolidating multiple loans into one manageable payment."
            },
            {
                'icon': 'clock',  # Icône pour l'horloge (prêt à court terme)
                'title': "Bridge Loans",
                'description': "Short-term financing solutions to bridge temporary gaps in funding or seize time-sensitive opportunities."
            }
        ]
        
        loan_steps = [
            {
                'step': "1",
                'title': "Application",
                'description': "Complete our streamlined online application in minutes."
            },
            {
                'step': "2",
                'title': "Documentation",
                'description': "Submit required documents through our secure portal."
            },
            {
                'step': "3",
                'title': "Review",
                'description': "Our team reviews your application within 24 hours."
            },
            {
                'step': "4",
                'title': "Approval",
                'description': "Receive your loan decision and terms."
            },
            {
                'step': "5",
                'title': "Funding",
                'description': "Get funded within 2-3 business days upon approval."
            }
        ]
        
        # Envoyer les données vers le template
        context = {
            'services': services,
            'loan_steps': loan_steps
        }
        
        return render(request, 'app/home-services.html', context)
    
class AboutView(TemplateView):
    template_name = 'app/home-about.html'

