from zipfile import ZipFile

from firebase_admin import storage

from django.shortcuts import render
from django.views.generic import TemplateView
from django.core.files.storage import FileSystemStorage

from main.settings import BASE_DIR


class UserProfile(TemplateView):
    bucket = storage.bucket()
    template_name = 'pages/user_profile/form.html'

    def post(self, request):
        email = request.POST.get('email')
        file = request.FILES.get('file')
        name = str(file.name)
        imgs_urls = []

        print(f'EMAIL: {email}')
        print(f'FILE: {file}')
        fss = FileSystemStorage()
        file = fss.save(BASE_DIR/'files'/name, file)

        with ZipFile(BASE_DIR/'files'/name) as zip:
            zip.extractall(BASE_DIR/'files')
            for filename in zip.namelist():
                blob = self.bucket.blob(f'images/{filename}')
                blob.upload_from_filename(BASE_DIR/'files'/filename)
                blob.make_public()
                imgs_urls.append(blob.public_url)
                fss.delete(BASE_DIR/'files'/filename)
        fss.delete(file)

        return render(request, self.template_name, {'urls': imgs_urls})
