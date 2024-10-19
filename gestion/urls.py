from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    AuteurViewSet,
    LivreViewSet,
    CategorieViewSet,
    ExemplaireViewSet,
    EmpruntViewSet,
    CommentaireViewSet,
    EvaluationViewSet,
    EditeurViewSet,
    LogoutView,
    SignupView,
    CustomTokenObtainPairView,
    CustomTokenRefreshView
)

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

# Ajout des routes au urlpatterns
urlpatterns = [
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('', include(router.urls)),
]
