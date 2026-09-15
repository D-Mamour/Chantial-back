"""API documentaire."""
from rest_framework import viewsets,decorators
from rest_framework.response import Response
from .models import Justificatif,ExtractionOCR,DocumentProjet
from .serializers import JustificatifSerializer,ExtractionOCRSerializer,DocumentProjetSerializer
from intelligence.services.rag import ServiceRAG

class JustificatifViewSet(viewsets.ModelViewSet):
    """CRUD des justificatifs."""
    serializer_class=JustificatifSerializer
    queryset=Justificatif.objects.all()

class ExtractionOCRViewSet(viewsets.ReadOnlyModelViewSet):
    """Lecture des résultats OCR."""
    serializer_class=ExtractionOCRSerializer
    queryset=ExtractionOCR.objects.all()

class DocumentProjetViewSet(viewsets.ModelViewSet):
    """CRUD des documents du projet."""
    serializer_class=DocumentProjetSerializer
    queryset=DocumentProjet.objects.all()
    def perform_create(self,serializer):
        """Associe l'auteur du dépôt."""
        serializer.save(ajoute_par=self.request.user)
    @decorators.action(detail=True,methods=["post"])
    def indexer_rag(self,request,pk=None):
        """Déclenche l'indexation du document."""
        d=self.get_object()
        ServiceRAG().indexer_document(d)
        return Response({"detail":"Document indexé.","id":str(d.id)})
