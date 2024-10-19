from django.contrib import admin
from .models import Auteur, Livre, Categorie, Exemplaire, Emprunt, Commentaire, Evaluation, Editeur, UserAccount

@admin.register(UserAccount)
class UserAccountAdmin(admin.ModelAdmin):
    search_fields = ['username']
    def get_list_display(self, request):
        return [field.name for field in UserAccount._meta.get_fields() if not field.many_to_many and not field.one_to_many and not field.name == "password"]

@admin.register(Auteur)
class AuteurAdmin(admin.ModelAdmin):
    search_fields = ['nom']
    list_display = ('nom', 'date_de_naissance')
    list_filter = ('date_de_naissance',)

@admin.register(Livre)
class LivreAdmin(admin.ModelAdmin):
    search_fields = ['titre', 'auteurs']
    list_display = ('titre', 'editeur', 'date_de_publication')
    list_filter = ('categorie', 'editeur')

@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    search_fields = ['nom']
    list_display = ('nom',) 

@admin.register(Exemplaire)
class ExemplaireAdmin(admin.ModelAdmin):
    list_display = ('livre', 'état')
    list_filter = ('état',)

@admin.register(Emprunt)
class EmpruntAdmin(admin.ModelAdmin):
    search_fields = ['exemplaire__livre__titre', 'utilisateur']
    list_display = ('exemplaire', 'utilisateur', 'date_emprunt', 'date_retour_effective')
    list_filter = ('date_retour_effective',)

@admin.register(Commentaire)
class CommentaireAdmin(admin.ModelAdmin):
    list_display = ('livre', 'utilisateur', 'date_publication', 'contenu')
    search_fields = ['livre__titre', 'utilisateur']
    list_filter = ('date_publication',)

@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    list_display = ('livre', 'utilisateur', 'note', 'date_évaluation')
    search_fields = ['livre__titre', 'utilisateur']
    list_filter = ('note',)

@admin.register(Editeur)
class EditeurAdmin(admin.ModelAdmin):
    search_fields = ['nom']
    list_display = ('nom', 'adresse', 'site_web')