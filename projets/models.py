"""Modèles de gestion des chantiers."""
import uuid
from decimal import Decimal
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Sum

class Projet(models.Model):
    """Représente un chantier géré par un entrepreneur pour un bailleur."""
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    entrepreneur=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT,related_name="projets_entrepreneur")
    bailleur=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT,related_name="projets_bailleur")
    nom=models.CharField(max_length=180)
    description=models.TextField(blank=True)
    localisation=models.CharField(max_length=255,blank=True)
    budget_previsionnel=models.DecimalField(max_digits=16,decimal_places=2,validators=[MinValueValidator(Decimal("0"))])
    date_debut=models.DateField()
    date_fin_prevue=models.DateField()
    statut=models.CharField(max_length=20,default="PLANIFIE")
    date_creation=models.DateTimeField(auto_now_add=True)

    @property
    def montant_depense(self):
        """Additionne toutes les dépenses rattachées aux étapes."""
        return self.etapes.aggregate(total=Sum("depenses__montant"))["total"] or Decimal("0")

    @property
    def budget_restant(self):
        """Retourne la différence entre budget prévu et dépenses."""
        return self.budget_previsionnel-self.montant_depense

    @property
    def avancement_global(self):
        """Calcule la moyenne du dernier avancement de chaque étape."""
        vals=[e.avancement_actuel for e in self.etapes.all()]
        return sum(vals,Decimal("0"))/len(vals) if vals else Decimal("0")

class Etape(models.Model):
    """Représente une phase du chantier."""
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    projet=models.ForeignKey(Projet,on_delete=models.CASCADE,related_name="etapes")
    nom=models.CharField(max_length=150)
    description=models.TextField(blank=True)
    ordre=models.PositiveIntegerField()
    budget_previsionnel=models.DecimalField(max_digits=16,decimal_places=2,validators=[MinValueValidator(Decimal("0"))])
    date_debut_prevue=models.DateField()
    date_fin_prevue=models.DateField()

    class Meta:
        ordering=["ordre"]
        unique_together=("projet","ordre")

    @property
    def avancement_actuel(self):
        """Retourne le dernier pourcentage déclaré."""
        dernier=self.avancements.order_by("-date_declaration").first()
        return dernier.pourcentage if dernier else Decimal("0")

class Avancement(models.Model):
    """Historise l'évolution d'une étape."""
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    etape=models.ForeignKey(Etape,on_delete=models.CASCADE,related_name="avancements")
    auteur=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT,related_name="avancements_declares")
    pourcentage=models.DecimalField(max_digits=5,decimal_places=2,validators=[MinValueValidator(0),MaxValueValidator(100)])
    commentaire=models.TextField(blank=True)
    date_declaration=models.DateTimeField(auto_now_add=True)
