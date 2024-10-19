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
    EditeurViewSet,
    LogoutView,
    SignupView,
    LoginView,
    RefreshView,
    OTPVerificationView,
    csrf_token_view
)

router = DefaultRouter()

router.register(r'auteurs', AuteurViewSet)
router.register(r'livres', LivreViewSet)
router.register(r'categories', CategorieViewSet)
router.register(r'exemplaires', ExemplaireViewSet)
router.register(r'emprunts', EmpruntViewSet)
router.register(r'commentaires', CommentaireViewSet)
router.register(r'evaluations', EvaluationViewSet)
router.register(r'editeurs', EditeurViewSet)

urlpatterns = [
    path('csrf-token/', csrf_token_view, name='csrf_token'),
    path('auth/token/', LoginView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', RefreshView.as_view(), name='token_refresh'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('auth/signup/', SignupView.as_view(), name='signup'),
    path('auth/verify-otp/', OTPVerificationView.as_view(), name='verify-otp'),
    path('', include(router.urls)),
]
