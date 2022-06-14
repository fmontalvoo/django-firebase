from firebase_admin import storage

from django.shortcuts import render
from django.views.generic import TemplateView
from django.core.files.storage import FileSystemStorage

from main.settings import BASE_DIR


class UserProfile(TemplateView):
    bucket = storage.bucket()
    template_name = 'pages/user_profile/form.html'

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        imgs = request.FILES.getlist('images')
        imgs_urls = []

        print(f'EMAIL: {email}')

        for img in imgs:
            fss = FileSystemStorage()
            file = fss.save(img.name, img)

            blob = self.bucket.blob(f'images/{file}')
            blob.upload_from_filename(BASE_DIR/file)
            fss.delete(file)
            blob.make_public()
            imgs_urls.append(blob.public_url)

        return render(request, self.template_name, {'urls': imgs_urls})
