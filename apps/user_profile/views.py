import re
from zipfile import ZipFile

from firebase_admin import storage

from main.settings import MEDIA_ROOT

from django.shortcuts import render
from django.views.generic import TemplateView
from django.core.files.storage import FileSystemStorage

from .models import Perfil


class UserProfile(TemplateView):
    bucket = storage.bucket()
    fss = FileSystemStorage()
    template_name = 'pages/user_profile/form.html'

    def post(self, request):
        email = request.POST.get('email')
        file = request.FILES.get('file')
        name = str(file.name)
        dir = name.split('.')[0]
        imgs_urls = []

        perfil = Perfil()
        perfil.email = email
        perfil.file = f'/media/{dir}'
        perfil.save()

        print(f'FILE: {file}')
        print(f'EMAIL: {email}')
        file = self.fss.save(MEDIA_ROOT/name, file)

        with ZipFile(MEDIA_ROOT/name) as zip:
            zip.extractall(MEDIA_ROOT)
            for filename in zip.namelist():
                if re.search(r'\.(?:jpe?g|gif|png)$', filename):
                    blob = self.bucket.blob(f'images/{filename}')
                    blob.upload_from_filename(MEDIA_ROOT/filename)
                    blob.make_public()
                    imgs_urls.append(blob.public_url)
                    # fss.delete(MEDIA_ROOT/filename)
        self.fss.delete(file)

        return render(request, self.template_name, {'urls': imgs_urls})
