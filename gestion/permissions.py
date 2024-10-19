from rest_framework import permissions
from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdmin(BasePermission):
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.groups.filter(name='admin').exists()

class IsLecteur(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.groups.filter(name='lecteur').exists()
        return False