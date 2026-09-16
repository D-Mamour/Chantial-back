"""Couche d'abstraction du moteur OCR."""
from decimal import Decimal, InvalidOperation
import re

class ServiceOCR:
    """Extrait et normalise les informations d'une facture ou d'un justificatif."""
    @staticmethod
    def normaliser_montant(valeur):
        """Transforme un montant textuel en Decimal."""
        if valeur is None: return None
        propre=re.sub(r"[^\d,.\-]","",str(valeur))
        if "," in propre and "." not in propre: propre=propre.replace(",",".")
        try: return Decimal(propre)
        except (InvalidOperation,ValueError): return None

    def extraire(self, fichier):
        """Point d'intégration du moteur OCR réel.

        Le projet garde volontairement le fournisseur OCR interchangeable.
        """
        return {"numero_document":"","fournisseur":"","date_document":None,
                "montant_extrait":None,"texte_extrait":""}
