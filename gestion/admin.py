from django.contrib import admin
from .models import Auteur, Livre, Categorie, Editeur

admin.site.register(Auteur)
admin.site.register(Livre)
admin.site.register(Categorie)
admin.site.register(Editeur)
