"""Sérialise les modèles de l’application finances."""
from rest_framework import serializers
from .models import Depense

class DepenseSerializer(serializers.ModelSerializer):
    """Sérialise le modèle Depense."""
    class Meta:
        model=Depense
        fields="__all__"
        read_only_fields=["id"]

