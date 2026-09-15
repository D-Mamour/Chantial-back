# Chantial Backend

Backend REST de **Chantial**, plateforme intelligente de suivi et de contrôle des projets BTP.

## 1. Stack technique

- Python 3.12 recommandé
- Django 5
- Django REST Framework
- JWT avec SimpleJWT
- PostgreSQL
- Angular côté frontend
- OCR : PDF texte + Tesseract pour les images
- RAG : récupération TF-IDF + génération locale via hangingface
- Documentation API : OpenAPI / Swagger

## 2. Logique métier

- **Entrepreneur** : crée ses projets, définit les étapes, déclare l'avancement, enregistre les dépenses et ajoute les justificatifs/documents.
- **Chantial** : centralise, extrait les données OCR, détecte des écarts, analyse le projet et produit des recommandations.
- **Bailleur** : ne modifie pas le chantier ; il consulte sa construction, vérifie les dépenses, valide/rejette et demande une justification/correction.
- **Administrateur** : gère les comptes et supervise la plateforme.

La plateforme ne conclut jamais automatiquement à une fraude. Elle parle d'**écart constaté**, de **vérification recommandée** et d'**action recommandée**.
