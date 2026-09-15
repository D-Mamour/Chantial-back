"""Documents, justificatifs et résultats OCR."""
import uuid
from django.conf import settings
from django.db import models
from finances.models import Depense
from projets.models import Projet

class Justificatif(models.Model):
    """Stocke une preuve associée à une dépense."""
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    depense=models.ForeignKey(Depense,on_delete=models.CASCADE,related_name="justificatifs")
    fichier=models.FileField(upload_to="justificatifs/%Y/%m/")
    type_document=models.CharField(max_length=80,blank=True)
    date_ajout=models.DateTimeField(auto_now_add=True)

class ExtractionOCR(models.Model):
    """Persiste les informations extraites d'un justificatif."""
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    justificatif=models.OneToOneField(Justificatif,on_delete=models.CASCADE,related_name="extraction_ocr")
    numero_document=models.CharField(max_length=100,blank=True)
    fournisseur=models.CharField(max_length=180,blank=True)
    date_document=models.DateField(null=True,blank=True)
    montant_extrait=models.DecimalField(max_digits=16,decimal_places=2,null=True,blank=True)
    texte_extrait=models.TextField(blank=True)
    date_extraction=models.DateTimeField(auto_now_add=True)

class DocumentProjet(models.Model):
    """Stocke un devis, contrat ou autre source documentaire utilisée par le RAG."""
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    projet=models.ForeignKey(Projet,on_delete=models.CASCADE,related_name="documents")
    ajoute_par=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT,related_name="documents_ajoutes")
    nom=models.CharField(max_length=180)
    type_document=models.CharField(max_length=80)
    fichier=models.FileField(upload_to="documents_projet/%Y/%m/")
    texte_extrait=models.TextField(blank=True)
    est_indexe=models.BooleanField(default=False)
    date_ajout=models.DateTimeField(auto_now_add=True)
