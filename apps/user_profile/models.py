from django.db import models


class Perfil(models.Model):
    id = models.AutoField(primary_key=True)
    file = models.URLField('File')
    email = models.EmailField('Correo Electrónico')

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfiles'
        ordering = ('id',)

    def __str__(self):
        return f'ID: {self.id}, Email: {self.email}, File: {self.file}'
