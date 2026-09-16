"""Sérialise les modèles de l’application projets."""
from rest_framework import serializers
from .models import Projet, Etape, Avancement

class ProjetSerializer(serializers.ModelSerializer):
    """Sérialise le modèle Projet."""
    class Meta:
        model=Projet
        fields="__all__"
        read_only_fields=["id"]

class EtapeSerializer(serializers.ModelSerializer):
    """Sérialise le modèle Etape."""
    class Meta:
        model=Etape
        fields="__all__"
        read_only_fields=["id"]

class AvancementSerializer(serializers.ModelSerializer):
    """Sérialise le modèle Avancement."""
    class Meta:
        model=Avancement
        fields="__all__"
        read_only_fields=["id"]

