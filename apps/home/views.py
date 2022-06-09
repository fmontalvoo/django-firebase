from django.views.generic import TemplateView

# Create your views here.
class Inicio(TemplateView):
    template_name = 'index.html'