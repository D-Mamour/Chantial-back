"""API des projets, étapes et avancements."""
from rest_framework import viewsets
from comptes.models import Utilisateur
from .models import Projet,Etape,Avancement
from .serializers import ProjetSerializer,EtapeSerializer,AvancementSerializer

def projets_accessibles(utilisateur):
    """Construit le queryset des projets visibles selon le rôle."""
    if utilisateur.role==Utilisateur.Role.ENTREPRENEUR:
        return Projet.objects.filter(entrepreneur=utilisateur)
    if utilisateur.role==Utilisateur.Role.BAILLEUR:
        return Projet.objects.filter(bailleur=utilisateur)
    return Projet.objects.all()

class ProjetViewSet(viewsets.ModelViewSet):
    """CRUD des projets avec isolation des données."""
    serializer_class=ProjetSerializer
    def get_queryset(self):
        """Retourne les projets autorisés."""
        return projets_accessibles(self.request.user)
    def perform_create(self,serializer):
        """Associe automatiquement l'entrepreneur connecté."""
        serializer.save(entrepreneur=self.request.user)

class EtapeViewSet(viewsets.ModelViewSet):
    """CRUD des étapes accessibles."""
    serializer_class=EtapeSerializer
    def get_queryset(self):
        """Filtre les étapes par projet accessible."""
        return Etape.objects.filter(projet__in=projets_accessibles(self.request.user))

class AvancementViewSet(viewsets.ModelViewSet):
    """CRUD de l'historique d'avancement."""
    serializer_class=AvancementSerializer
    def get_queryset(self):
        """Filtre les avancements par projet accessible."""
        return Avancement.objects.filter(etape__projet__in=projets_accessibles(self.request.user))
    def perform_create(self,serializer):
        """Enregistre l'utilisateur comme auteur."""
        serializer.save(auteur=self.request.user)
