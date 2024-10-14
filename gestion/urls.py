from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from .views import (
    AuteurViewSet,
    LivreViewSet,
    CategorieViewSet,
    ExemplaireViewSet,
    EmpruntViewSet,
    CommentaireViewSet,
    EvaluationViewSet,
    EditeurViewSet
)
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Créez un routeur pour gérer automatiquement les routes pour les ViewSets
router = DefaultRouter()

# Enregistrement des ViewSets dans le routeur
router.register(r'auteurs', AuteurViewSet)
router.register(r'livres', LivreViewSet)
router.register(r'categories', CategorieViewSet)
router.register(r'exemplaires', ExemplaireViewSet)
router.register(r'emprunts', EmpruntViewSet)
router.register(r'commentaires', CommentaireViewSet)
router.register(r'evaluations', EvaluationViewSet)
router.register(r'editeurs', EditeurViewSet)

# Configuration de la documentation Swagger
schema_view = get_schema_view(
   openapi.Info(
      title="Bibliothèque API",
      default_version='v1',
      description="Documentation de l'API pour la gestion de bibliothèque",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@bibliotheque.local"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

# Ajout des routes au urlpatterns
urlpatterns = [
    path('api/', include(router.urls)),  # Toutes les routes de l'API via le routeur
]
