"""Routes de l'application intelligence."""
from rest_framework.routers import DefaultRouter
from .views import AnalyseViewSet, AnomalieViewSet, RecommandationViewSet

router = DefaultRouter()
router.register(r"analyses", AnalyseViewSet, basename="analyses")
router.register(r"anomalies", AnomalieViewSet, basename="anomalies")
router.register(r"recommandations", RecommandationViewSet, basename="recommandations")

urlpatterns = router.urls
