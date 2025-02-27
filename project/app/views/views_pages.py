from django.views.generic import TemplateView

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
        
        
class AdvisorDashboardView(TemplateView):
    """
    Renders the advisor dashboard.

    This view is responsible for rendering the 'advisor_dashboard.html' template, which serves as the 
    dashboard for the advisors.

    Attributes:
        template_name (str): The name of the template used to display the response.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders the 'advisor_dashboard.html' template.
    """
    template_name = 'app/advisor-dashboard.html'