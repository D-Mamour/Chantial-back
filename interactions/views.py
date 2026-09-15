from django.shortcuts import render

# Create your views here.
"""API des demandes et alertes."""
from django.db.models import Q
from rest_framework import viewsets
from .models import Demande,Alerte
from .serializers import DemandeSerializer,AlerteSerializer

class DemandeViewSet(viewsets.ModelViewSet):
    """Gère les demandes envoyées ou reçues."""
    serializer_class=DemandeSerializer
    def get_queryset(self):
        """Retourne uniquement les demandes liées au compte."""
        return Demande.objects.filter(Q(auteur=self.request.user)|Q(destinataire=self.request.user))
    def perform_create(self,serializer):
        """Associe l'auteur connecté."""
        serializer.save(auteur=self.request.user)

class AlerteViewSet(viewsets.ReadOnlyModelViewSet):
    """Expose les alertes personnelles."""
    serializer_class=AlerteSerializer
    def get_queryset(self):
        """Retourne uniquement les alertes du compte."""
        return Alerte.objects.filter(utilisateur=self.request.user)
