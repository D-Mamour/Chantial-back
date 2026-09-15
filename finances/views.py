"""API financière."""
from rest_framework import viewsets,decorators
from rest_framework.response import Response
from comptes.models import Utilisateur
from audit.services import ServiceAudit
from .models import Depense
from .serializers import DepenseSerializer

class DepenseViewSet(viewsets.ModelViewSet):
    """CRUD et validation des dépenses."""
    serializer_class=DepenseSerializer
    def get_queryset(self):
        """Isole les dépenses selon le rôle."""
        u=self.request.user
        if u.role==Utilisateur.Role.ENTREPRENEUR:
            return Depense.objects.filter(etape__projet__entrepreneur=u)
        if u.role==Utilisateur.Role.BAILLEUR:
            return Depense.objects.filter(etape__projet__bailleur=u)
        return Depense.objects.all()

    def perform_create(self,serializer):
        """Associe l'auteur connecté."""
        serializer.save(auteur=self.request.user)

    @decorators.action(detail=True,methods=["post"])
    def valider(self,request,pk=None):
        """Valide une dépense uniquement si l'utilisateur est son bailleur."""
        d=self.get_object()
        if request.user!=d.projet.bailleur:
            return Response({"detail":"Action réservée au bailleur du projet."},status=403)
        d.statut=Depense.Statut.VALIDEE; d.save(update_fields=["statut"])
        ServiceAudit.enregistrer("VALIDATION_DEPENSE",request.user,d.projet)
        return Response(self.get_serializer(d).data)

    @decorators.action(detail=True,methods=["post"])
    def rejeter(self,request,pk=None):
        """Rejette une dépense uniquement si l'utilisateur est son bailleur."""
        d=self.get_object()
        if request.user!=d.projet.bailleur:
            return Response({"detail":"Action réservée au bailleur du projet."},status=403)
        d.statut=Depense.Statut.REJETEE; d.save(update_fields=["statut"])
        ServiceAudit.enregistrer("REJET_DEPENSE",request.user,d.projet)
        return Response(self.get_serializer(d).data)
