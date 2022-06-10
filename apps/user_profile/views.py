from django.views.generic import TemplateView

# Create your views here.
class UserProfile(TemplateView):
    template_name = 'pages/user_profile/form.html'
