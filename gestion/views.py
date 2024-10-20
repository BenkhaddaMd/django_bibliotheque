from rest_framework import viewsets
from rest_framework.views import APIView
from .models import Auteur, Livre, Categorie, Emprunt, Commentaire, Evaluation, Editeur, Exemplaire, UserAccount
from .serializers import TokenObtainPairSerializer, SignupSerializer, AuteurSerializer, LivreSerializer, CategorieSerializer, EmpruntSerializer, CommentaireSerializer, EvaluationSerializer, EditeurSerializer, ExemplaireSerializer
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
from rest_framework.authtoken.models import Token
import jwt
import pyotp
from django.conf import settings
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect

def csrf_token_view(request):
    csrf_token = get_token(request)
    return JsonResponse({'csrfToken': csrf_token})

@method_decorator(csrf_protect, name='dispatch')
class LoginView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

@method_decorator(csrf_protect, name='dispatch')
class OTPVerificationView(APIView):

    def verify_otp(self, user, otp_token):
        totp = pyotp.TOTP(user.otp_secret)
        return totp.verify(otp_token)

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def post(self, request):
        tmp_token = request.data.get('tmp_token')
        otp_token = request.data.get('otp_token')

        try:
            payload = jwt.decode(tmp_token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = payload.get('user_id')
            user = UserAccount.objects.get(id=user_id)
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Temporary token expired'}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return Response({'error': 'Invalid temporary token'}, status=status.HTTP_401_UNAUTHORIZED)

        if self.verify_otp(user, otp_token):
            tokens = self.get_tokens_for_user(user)
            return Response(tokens, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid OTP token'}, status=status.HTTP_401_UNAUTHORIZED)

@method_decorator(csrf_protect, name='dispatch')
class RefreshView(TokenRefreshView):
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

@method_decorator(csrf_protect, name='dispatch')
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

@method_decorator(csrf_protect, name='dispatch')
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

@method_decorator(csrf_protect, name='dispatch')
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

@method_decorator(csrf_protect, name='dispatch')
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

@method_decorator(csrf_protect, name='dispatch')
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

@method_decorator(csrf_protect, name='dispatch')
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

@method_decorator(csrf_protect, name='dispatch')
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

@method_decorator(csrf_protect, name='dispatch')
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

@method_decorator(csrf_protect, name='dispatch')
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

@method_decorator(csrf_protect, name='dispatch')
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
