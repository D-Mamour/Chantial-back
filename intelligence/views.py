"""API d'analyse intelligente."""
from rest_framework import viewsets,decorators
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from projets.views import projets_accessibles
from .models import Analyse,Anomalie,Recommandation
from .serializers import AnalyseSerializer,AnomalieSerializer,RecommandationSerializer
from .services.analyse import ServiceAnalyse

class AnalyseViewSet(viewsets.ReadOnlyModelViewSet):
    """Expose et déclenche les analyses."""
    serializer_class=AnalyseSerializer
    def get_queryset(self):
        """Filtre les analyses par projets accessibles."""
        return Analyse.objects.filter(projet__in=projets_accessibles(self.request.user))
    @decorators.action(detail=False,methods=["post"])
    def lancer(self,request):
        """Lance règles métier et préparation RAG."""
        projet=get_object_or_404(projets_accessibles(request.user),pk=request.data.get("projet"))
        analyse,rag=ServiceAnalyse().analyser_projet(projet)
        return Response({"analyse":self.get_serializer(analyse).data,"rag":rag})

class AnomalieViewSet(viewsets.ReadOnlyModelViewSet):
    """Expose les anomalies accessibles."""
    serializer_class=AnomalieSerializer
    def get_queryset(self):
        """Filtre par projet accessible."""
        return Anomalie.objects.filter(projet__in=projets_accessibles(self.request.user))

class RecommandationViewSet(viewsets.ReadOnlyModelViewSet):
    """Expose les recommandations accessibles."""
    serializer_class=RecommandationSerializer
    def get_queryset(self):
        """Filtre par projet accessible."""
        return Recommandation.objects.filter(projet__in=projets_accessibles(self.request.user))
