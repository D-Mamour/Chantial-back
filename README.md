# Chantial — Backend Django modulaire

Cette version organise le backend par **domaines métier** et non par diagrammes de séquence.

## Applications

- `comptes` : utilisateur, rôles, JWT et profil.
- `projets` : projet, étape et avancement.
- `finances` : dépenses, validation et rejet.
- `documents` : justificatifs, documents projet et OCR.
- `intelligence` : analyse, anomalies, recommandations et RAG.
- `interactions` : demandes et alertes.
- `audit` : historique et traçabilité.

## Architecture

chantial_backend/
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── comptes/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── permissions.py
│   └── urls.py
├── projets/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── services.py
│   └── urls.py
├── finances/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── services.py
│   └── urls.py
├── documents/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── services/
│   │   ├── ocr.py
│   │   └── extraction.py
│   └── urls.py
├── intelligence/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── services/
│   │   ├── rag.py
│   │   ├── embeddings.py
│   │   ├── analyse.py
│   │   └── recommandations.py
│   └── urls.py
├── interactions/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
├── audit/
│   ├── models.py
│   └── services.py
├── manage.py
├── requirements.txt
└── .env

## Démarrage

```bash
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
docker compose up -d
python manage.py makemigrations comptes projets finances documents intelligence interactions audit
python manage.py migrate
python manage.py check
python manage.py createsuperuser
python manage.py test
python manage.py runserver
```

Swagger : `http://127.0.0.1:8000/api/docs/`

## Important concernant l'IA

L'architecture RAG est séparée et prête à recevoir un moteur d'embeddings, une base
vectorielle et un LLM. Cette archive **ne prétend pas fournir un RAG de production
déjà branché** : `ServiceRAG` expose les points d'intégration nécessaires.
Même une fois le LLM connecté, la validation finale d'une dépense reste une décision
du bailleur.

Le service OCR suit la même logique : son interface est prête, mais le moteur OCR réel
(Tesseract, EasyOCR ou fournisseur externe) doit être configuré.
