#  HR-Pulse Backend API

Le moteur intelligent de HR-Pulse, exploitant l'IA Azure et le Machine Learning pour l'analyse du marché de l'emploi.

## Fonctionnalités

- **Authentification Sécurisée** : Inscription et connexion avec hachage de mot de passe (Argon2) et validation par jeton JWT.
- **Analyse NER (Azure AI)** : Extraction intelligente des compétences critiques à partir des offres d'emploi grâce au Named Entity Recognition.
- **Prédiction Salariale ML** : Modèle de régression (Scikit-learn) pour estimer le salaire moyen basé sur les compétences et l'intitulé du poste.
- **Répertoire SQL** : Recherche ultra-rapide parmi des milliers de titres de postes indexés dans Azure SQL.

##  Stack Technique

- **Framework** : [FastAPI](https://fastapi.tiangolo.com/) (Python 3.12+)
- **Gestionnaire de dépendances** : [uv](https://github.com/astral-sh/uv)
- **Base de données** : Azure SQL / MSSQL (via SQLAlchemy & PyODBC)
- **IA/ML** : 
  - Azure AI Language (Text Analytics)
  - Scikit-learn (Modèle prédictif)
- **Déploiement** : Docker / Docker Compose

## Installation & Configuration

### 1. Prérequis
- Python 3.12+
- `uv` installé (`curl -LsSf https://astral.sh/uv/install.sh | sh`)

### 2. Installation locale
```bash
# Synchroniser les dépendances
uv sync

# Configurer l'environnement
cp .env.example .env
# Remplissez .env avec vos clés Azure et vos accès SQL
```

### 3. Lancement
```bash
# Mode développement
uv run uvicorn src.api.main:app --reload

# Avec Docker
docker build -t hr-pulse-backend .
docker run -p 8000:8000 hr-pulse-backend
```

##  Structure du projet

- `src/api/routers/` : Points de terminaison (Auth, Jobs, Predict).
- `src/api/crud/` : Opérations sur la base de données.
- `src/api/schemas/` : Modèles Pydantic pour la validation des données.
- `src/core/` : Logique de sécurité et configuration système.
- `src/database/` : Session SQLAlchemy et modèles de tables.
- `ml_models_saved/` : Modèles Scikit-learn entraînés et exportés.

##  Points de terminaison (Endpoints)

| Méthode | Route | Description |
| :--- | :--- | :--- |
| `POST` | `/auth/register` | Création de compte utilisateur |
| `POST` | `/auth/login` | Authentification et génération de Token JWT |
| `GET` | `/jobs/titles` | Liste tous les titres de postes disponibles |
| `GET` | `/jobs/search` | Recherche par compétences (Extraction NER) |
| `POST` | `/predict/predict` | Prédiction salariale via IA |

---
**Documentation Interactive** : Une fois le serveur lancé, accédez au Swagger sur [http://localhost:8000/docs](http://localhost:8000/docs)