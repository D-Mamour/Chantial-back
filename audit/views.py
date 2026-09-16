"""API de consultation de l'audit."""
from rest_framework import viewsets
from .models import Historique
from .serializers import HistoriqueSerializer

class HistoriqueViewSet(viewsets.ReadOnlyModelViewSet):
    """Expose l'historique ; l'écriture passe par ServiceAudit."""
    serializer_class=HistoriqueSerializer
    def get_queryset(self):
        """Limite l'historique au compte sauf pour l'administrateur."""
        u=self.request.user
        return Historique.objects.all() if u.role=="ADMINISTRATEUR" else Historique.objects.filter(utilisateur=u)
