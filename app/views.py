from django.views.generic import TemplateView


class HomeView(TemplateView):
    """A home view that gets data from the API."""

    template_name = 'home.html'
