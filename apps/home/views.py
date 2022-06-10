from firebase_admin import firestore
from django.views.generic import TemplateView

# Create your views here.
class Inicio(TemplateView):
    db = firestore.client()
    doc_ref = db.collection(u'items').document()
    doc_ref.set({
        u'titulo': u'Prueba',
        u'Descripcion': u'Esto es una prueba',
    })
    template_name = 'index.html'