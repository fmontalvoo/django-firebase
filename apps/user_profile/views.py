from firebase_admin import storage

from django.shortcuts import render
from django.views.generic import TemplateView
from django.core.files.storage import FileSystemStorage

from main.settings import BASE_DIR

# Create your views here.


class UserProfile(TemplateView):
    bucket = storage.bucket()
    template_name = 'pages/user_profile/form.html'

    def post(self, request, *args, **kwargs):
        img = request.FILES.get('imagen')
        correo = request.POST.get('correo')
        fss = FileSystemStorage()
        file = fss.save(img.name, img)

        blob = self.bucket.blob(f'images/{file}')
        blob.upload_from_filename(BASE_DIR/file)
        fss.delete(file)
        blob.make_public()
        return render(request, self.template_name, {'url': blob.public_url})
