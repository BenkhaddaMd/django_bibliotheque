from rest_framework import serializers
from .models import Auteur, Livre, Categorie, Exemplaire, Emprunt, Commentaire, Evaluation, Editeur, UserAccount
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator, ValidationError
import re
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
import pyotp
from django.contrib.auth import authenticate
import datetime
import jwt
from django.conf import settings

def generate_tmp_token(user):
    payload = {
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=2),
        'iat': datetime.datetime.utcnow()
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token

class TokenObtainPairSerializer(TokenObtainPairSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        user = authenticate(username=attrs['username'], password=attrs['password'])

        if user is not None:
            tmp_token = generate_tmp_token(user)
            return {"tmp_token": tmp_token}
        else:
            raise serializers.ValidationError('Invalid credentials')

class SignupSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=UserAccount.objects.all())]
    )
    password = serializers.CharField(
        write_only=True, 
        required=True, 
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = UserAccount
        fields = ('username', 'email', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Les mots de passe ne correspondent pas."})

        if len(attrs['password']) < 13:
            raise serializers.ValidationError({"password_too_short": "Le mot de passe doit contenir au moins 13 caractères."})

        if not re.findall(r'[A-Z]', attrs['password']):
            raise serializers.ValidationError( {"password_no_upper":"Le mot de passe doit contenir au moins une lettre majuscule."})

        if not re.findall(r'[a-z]', attrs['password']):
            raise serializers.ValidationError({"password_no_lower":"Le mot de passe doit contenir au moins une lettre minuscule."})

        if not re.findall(r'[0-9]', attrs['password']):
            raise serializers.ValidationError({"password_no_digit":"Le mot de passe doit contenir au moins un chiffre."})

        if not re.findall(r'[!@#$%^&*(),.?":{}|<>]', attrs['password']):
            raise serializers.ValidationError({"password_no_special":"Le mot de passe doit contenir au moins un caractère spécial."})
        return attrs

    def create(self, validated_data):
        otp_secret = pyotp.random_base32()

        user = UserAccount.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            otp_secret=otp_secret
        )
        user.set_password(validated_data['password'])
        user.save()
        return user, otp_secret

class AuteurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auteur
        fields = '__all__'

class LivreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Livre
        fields = '__all__'

class CategorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorie
        fields = '__all__'

class CommentaireSerializer(serializers.ModelSerializer):
    utilisateur = serializers.StringRelatedField()
    livre = serializers.StringRelatedField()

    class Meta:
        model = Commentaire
        fields = '__all__'

class EvaluationSerializer(serializers.ModelSerializer):
    utilisateur = serializers.StringRelatedField()
    livre = serializers.StringRelatedField()

    class Meta:
        model = Evaluation
        fields = '__all__'

class EditeurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Editeur
        fields = '__all__'

class ExemplaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exemplaire
        fields = '__all__'

class EmpruntSerializer(serializers.ModelSerializer):
    utilisateur = serializers.StringRelatedField()
    exemplaire = serializers.StringRelatedField()

    class Meta:
        model = Emprunt
        fields = '__all__'
