"""Services métier relatifs aux projets et à l'avancement."""
from decimal import Decimal


class ServiceProjet:
    """Centralise les calculs métier d'un chantier."""

    @staticmethod
    def calculer_avancement_global(projet):
        """Calcule la moyenne du dernier avancement connu de chaque étape."""
        valeurs = [etape.avancement_actuel for etape in projet.etapes.all()]
        return sum(valeurs, Decimal("0")) / len(valeurs) if valeurs else Decimal("0")

    @staticmethod
    def calculer_budget_restant(projet):
        """Retourne le budget prévisionnel diminué des dépenses enregistrées."""
        return projet.budget_previsionnel - projet.montant_depense

    @staticmethod
    def tableau_de_bord(projet):
        """Construit les principaux indicateurs affichés sur le tableau de bord."""
        return {
            "budget_previsionnel": projet.budget_previsionnel,
            "montant_depense": projet.montant_depense,
            "budget_restant": ServiceProjet.calculer_budget_restant(projet),
            "avancement_global": ServiceProjet.calculer_avancement_global(projet),
            "nombre_etapes": projet.etapes.count(),
        }
