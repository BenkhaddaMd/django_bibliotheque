from rest_framework import viewsets
from rest_framework.views import APIView
from .models import Auteur, Livre, Categorie, Emprunt, Commentaire, Evaluation, Editeur, Exemplaire
from .serializers import CustomTokenObtainPairSerializer, SignupSerializer, AuteurSerializer, LivreSerializer, CategorieSerializer, EmpruntSerializer, CommentaireSerializer, EvaluationSerializer, EditeurSerializer, ExemplaireSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .permissions import IsLecteur, IsAdmin
from rest_framework.permissions import SAFE_METHODS
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from io import BytesIO
import base64
import pyotp
import qrcode

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

class CustomTokenRefreshView(TokenRefreshView):
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user, otp_secret = serializer.save()
            otp_uri = pyotp.totp.TOTP(otp_secret).provisioning_uri(
                user.email, issuer_name="YourAppName"
            )

            qr = qrcode.make(otp_uri)
            buffer = BytesIO()
            qr.save(buffer, format="PNG")
            qr_code_image = base64.b64encode(buffer.getvalue()).decode('utf-8')

            return Response({
                "message": "Utilisateur créé avec succès",
                "qr_code": qr_code_image
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            print(refresh_token)
            token.blacklist()
            return Response({"detail": "Déconnexion réussie."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"detail": "Échec de la déconnexion."}, status=status.HTTP_400_BAD_REQUEST)

class CustomPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 100

class AuteurViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Auteur.objects.all()
    serializer_class = AuteurSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['nom', 'nationalité']
    ordering_fields = ['date_de_naissance', 'nom']
    pagination_class = CustomPagination

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            self.permission_classes = [IsAuthenticated, IsLecteur]
        else:
            self.permission_classes = [IsAuthenticated, IsAdmin]

        return super().get_permissions()

class LivreViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Livre.objects.all()
    serializer_class = LivreSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['titre', 'langue']
    ordering_fields = ['date_de_publication']
    pagination_class = CustomPagination

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            self.permission_classes = [IsAuthenticated, IsLecteur]
        else:
            self.permission_classes = [IsAuthenticated, IsAdmin]

        return super().get_permissions()

class CategorieViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Categorie.objects.all()
    serializer_class = CategorieSerializer

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            self.permission_classes = [IsAuthenticated, IsLecteur]
        else:
            self.permission_classes = [IsAuthenticated, IsAdmin]

        return super().get_permissions()

class EmpruntViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Emprunt.objects.all()
    serializer_class = EmpruntSerializer

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            self.permission_classes = [IsAuthenticated, IsLecteur]
        else:
            self.permission_classes = [IsAuthenticated, IsAdmin]

        return super().get_permissions()

class CommentaireViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Commentaire.objects.all()
    serializer_class = CommentaireSerializer

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            self.permission_classes = [IsAuthenticated, IsLecteur]
        else:
            self.permission_classes = [IsAuthenticated, IsAdmin]

        return super().get_permissions()

class EvaluationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Evaluation.objects.all()
    serializer_class = EvaluationSerializer

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            self.permission_classes = [IsAuthenticated, IsLecteur]
        else:
            self.permission_classes = [IsAuthenticated, IsAdmin]

        return super().get_permissions()

class EditeurViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Editeur.objects.all()
    serializer_class = EditeurSerializer

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            self.permission_classes = [IsAuthenticated, IsLecteur]
        else:
            self.permission_classes = [IsAuthenticated, IsAdmin]

        return super().get_permissions()

class ExemplaireViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Exemplaire.objects.all()
    serializer_class = ExemplaireSerializer

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            self.permission_classes = [IsAuthenticated, IsLecteur]
        else:
            self.permission_classes = [IsAuthenticated, IsAdmin]

        return super().get_permissions()
