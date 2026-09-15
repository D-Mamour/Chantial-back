"""Sérialise les modèles de l’application documents."""
from rest_framework import serializers
from .models import Justificatif, ExtractionOCR, DocumentProjet

class JustificatifSerializer(serializers.ModelSerializer):
    """Sérialise le modèle Justificatif."""
    class Meta:
        model=Justificatif
        fields="__all__"
        read_only_fields=["id"]

class ExtractionOCRSerializer(serializers.ModelSerializer):
    """Sérialise le modèle ExtractionOCR."""
    class Meta:
        model=ExtractionOCR
        fields="__all__"
        read_only_fields=["id"]

class DocumentProjetSerializer(serializers.ModelSerializer):
    """Sérialise le modèle DocumentProjet."""
    class Meta:
        model=DocumentProjet
        fields="__all__"
        read_only_fields=["id"]

