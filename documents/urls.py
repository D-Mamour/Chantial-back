"""Routes de l'application documents."""
from rest_framework.routers import DefaultRouter
from .views import JustificatifViewSet, ExtractionOCRViewSet, DocumentProjetViewSet

router = DefaultRouter()
router.register(r"justificatifs", JustificatifViewSet, basename="justificatifs")
router.register(r"extractions-ocr", ExtractionOCRViewSet, basename="extractions-ocr")
router.register(r"documents", DocumentProjetViewSet, basename="documents")

urlpatterns = router.urls
