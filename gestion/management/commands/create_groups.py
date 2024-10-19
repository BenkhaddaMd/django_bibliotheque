from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.apps import apps

class Command(BaseCommand):
    help = 'Crée des groupes "lecteur" et "admin" avec des permissions spécifiques pour tous les modèles'

    def handle(self, *args, **kwargs):
        # Créer le groupe 'lecteur'
        lecteur_group, created = Group.objects.get_or_create(name='lecteur')

        all_models = apps.get_app_config('gestion').get_models()

        permissions_to_add = []

        for model in all_models:
            model_name = model._meta.model_name
            
            # Ajouter uniquement la permission de lecture
            view_permission_codename = f'view_{model_name}'
            try:
                view_permission = Permission.objects.get(codename=view_permission_codename)
                permissions_to_add.append(view_permission)
            except Permission.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Permission {view_permission_codename} non trouvée pour {model_name}'))

        lecteur_group.permissions.set(permissions_to_add)

        # Créer le groupe 'admin'
        admin_group, created = Group.objects.get_or_create(name='admin')

        permissions_to_add_admin = []

        for model in all_models:
            model_name = model._meta.model_name
            
            # Ajouter toutes les permissions pour les modèles
            for perm in ['add', 'change', 'delete', 'view']:
                permission_codename = f'{perm}_{model_name}'
                try:
                    permission = Permission.objects.get(codename=permission_codename)
                    permissions_to_add_admin.append(permission)
                except Permission.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f'Permission {permission_codename} non trouvée pour {model_name}'))

        admin_group.permissions.set(permissions_to_add_admin)

        self.stdout.write(self.style.SUCCESS('Groupes et permissions créés avec succès.'))
