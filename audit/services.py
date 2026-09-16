"""Service de traçabilité."""
from .models import Historique
class ServiceAudit:
    """Centralise l'écriture de l'historique."""
    @staticmethod
    def enregistrer(action, utilisateur=None, projet=None, description="", donnees=None):
        """Crée une trace d'audit."""
        return Historique.objects.create(utilisateur=utilisateur,
            projet_id=getattr(projet,"id",None),action=action,
            description=description,donnees=donnees or {})
