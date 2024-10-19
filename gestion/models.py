from django.db import models
import pyotp
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

class UserAccount(AbstractUser):
    otp_secret = models.CharField(max_length=16, blank=True, null=True)

    def __str__(self):
        return self.email

    def get_otp(self):
        if not self.otp_secret:
            self.otp_secret = pyotp.random_base32()
            self.save()
        return pyotp.TOTP(self.otp_secret)

    def verify_otp(self, token):
        totp = self.get_otp()
        return totp.verify(token)

class Auteur(models.Model):
    nom = models.CharField(max_length=255)
    biographie = models.TextField()
    date_de_naissance = models.DateField()
    date_de_décès = models.DateField(null=True, blank=True)
    nationalité = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='auteurs_photos/', null=True, blank=True)

    def __str__(self):
        return self.nom

class Categorie(models.Model):
    nom = models.CharField(max_length=255)
    description = models.TextField()
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.nom

class Editeur(models.Model):
    nom = models.CharField(max_length=255)
    adresse = models.TextField()
    site_web = models.URLField()
    email_contact = models.EmailField()
    description = models.TextField()
    logo = models.ImageField(upload_to='editeurs_logos/', null=True, blank=True)

    def __str__(self):
        return self.nom

class Livre(models.Model):
    titre = models.CharField(max_length=255)
    résumé = models.TextField()
    date_de_publication = models.DateField()
    isbn = models.CharField(max_length=13, unique=True)
    nombre_de_pages = models.IntegerField()
    langue = models.CharField(max_length=100)
    image_de_couverture = models.ImageField(upload_to='livres_couvertures/', null=True, blank=True)
    format = models.CharField(max_length=50, choices=[('Broché', 'Broché'), ('Relié', 'Relié'), ('Numérique', 'Numérique')])
    auteurs = models.ManyToManyField(Auteur, related_name='livres')
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, related_name='livres')
    editeur = models.ForeignKey(Editeur, on_delete=models.SET_NULL, null=True, related_name='livres')

    def __str__(self):
        return self.titre

class Exemplaire(models.Model):
    livre = models.ForeignKey(Livre, on_delete=models.CASCADE, related_name='exemplaires')
    état = models.CharField(max_length=100)
    date_acquisition = models.DateField()
    localisation = models.CharField(max_length=255)
    disponibilité = models.BooleanField(default=True)

    def __str__(self):
        return f"Exemplaire de {self.livre.titre} - {self.état}"

class Emprunt(models.Model):
    exemplaire = models.ForeignKey(Exemplaire, on_delete=models.CASCADE, related_name='emprunts')
    utilisateur = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='emprunts')
    date_emprunt = models.DateTimeField(auto_now_add=True)
    date_retour_prévue = models.DateTimeField()
    date_retour_effective = models.DateTimeField(null=True, blank=True)
    statut = models.CharField(max_length=100, choices=[('En cours', 'En cours'), ('Terminé', 'Terminé'), ('En retard', 'En retard')])
    remarques = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Emprunt par {self.utilisateur.username} de {self.exemplaire.livre.titre}"

class Commentaire(models.Model):
    utilisateur = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='commentaires')
    livre = models.ForeignKey(Livre, on_delete=models.CASCADE, related_name='commentaires')
    contenu = models.TextField()
    date_publication = models.DateTimeField(auto_now_add=True)
    visible = models.BooleanField(default=True)
    modéré = models.BooleanField(default=False)

    def __str__(self):
        return f"Commentaire sur {self.livre.titre} par {self.utilisateur.username}"

class Evaluation(models.Model):
    utilisateur = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='evaluations')
    livre = models.ForeignKey(Livre, on_delete=models.CASCADE, related_name='evaluations')
    note = models.IntegerField()
    commentaire = models.TextField(null=True, blank=True)
    date_évaluation = models.DateTimeField(auto_now_add=True)
    recommandé = models.BooleanField(default=False)

    def __str__(self):
        return f"Évaluation de {self.livre.titre} par {self.utilisateur.username} - {self.note}/5"

