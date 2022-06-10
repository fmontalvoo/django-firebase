from django.urls import path
from .views import UserProfile

urlpatterns = [
    path('form', UserProfile.as_view(), name='formulario'),
]
