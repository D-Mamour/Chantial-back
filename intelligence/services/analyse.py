"""Règles métier et orchestration RAG."""
from decimal import Decimal
from django.utils import timezone
from intelligence.models import Analyse, Anomalie
from .recommandations import ServiceRecommandation
from .rag import ServiceRAG

class ServiceAnalyse:
    """Combine des contrôles déterministes et le contexte documentaire RAG."""
    def __init__(self, rag=None):
        """Permet d'injecter un autre service RAG pendant les tests."""
        self.rag=rag or ServiceRAG()

    def detecter_anomalies(self, projet):
        """Détecte dépassements et justificatifs manquants."""
        anomalies=[]
        for etape in projet.etapes.prefetch_related("depenses__justificatifs"):
            total=sum((d.montant for d in etape.depenses.all()),Decimal("0"))
            if total>etape.budget_previsionnel:
                anomalies.append(Anomalie.objects.create(
                    projet=projet,type_anomalie="DEPASSEMENT_BUDGET",niveau="ELEVE",
                    description=f"Écart constaté sur le budget de l'étape {etape.nom}."))
            for depense in etape.depenses.all():
                if not depense.justificatifs.exists():
                    anomalies.append(Anomalie.objects.create(
                        projet=projet,depense=depense,type_anomalie="JUSTIFICATIF_MANQUANT",
                        niveau="MODERE",description="Vérification recommandée : justificatif manquant."))
        return anomalies

    def evaluer_risque_retard(self, projet):
        """Produit un risque explicable à partir des dates et avancements."""
        aujourd_hui=timezone.localdate()
        retard=sum(1 for e in projet.etapes.all()
                   if e.date_fin_prevue<aujourd_hui and e.avancement_actuel<100)
        return ("ELEVE",Decimal("80")) if retard>=2 else (
               ("MODERE",Decimal("50")) if retard==1 else ("FAIBLE",Decimal("20")))

    def analyser_projet(self, projet):
        """Crée l'analyse, les anomalies et une recommandation éventuelle."""
        anomalies=self.detecter_anomalies(projet)
        niveau,score=self.evaluer_risque_retard(projet)
        rag=self.rag.analyser(projet,
            "Analyse les écarts du chantier à partir des documents disponibles.")
        analyse=Analyse.objects.create(projet=projet,niveau_risque=niveau,
            score_risque=score,resume=f"{len(anomalies)} anomalie(s), risque {niveau}.")
        if anomalies:
            ServiceRecommandation.creer(
                projet=projet,
                analyse=analyse,
                titre="Vérification recommandée",
                description="Contrôler les écarts et leurs sources avant validation.",
            )
        return analyse,rag
