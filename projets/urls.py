"""Routes de l'application projets."""
from rest_framework.routers import DefaultRouter
from .views import ProjetViewSet, EtapeViewSet, AvancementViewSet

router = DefaultRouter()
router.register(r"projets", ProjetViewSet, basename="projets")
router.register(r"etapes", EtapeViewSet, basename="etapes")
router.register(r"avancements", AvancementViewSet, basename="avancements")

urlpatterns = router.urls
