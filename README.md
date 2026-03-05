<<<<<<< HEAD
<div align="center">
  <img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi" alt="FastAPI" />
  <img src="https://img.shields.io/badge/Python_3.12-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Azure_SQL-0089D6?style=for-the-badge&logo=microsoft-azure&logoColor=white" alt="Azure SQL" />
  <img src="https://img.shields.io/badge/Azure_AI-0078D4?style=for-the-badge&logo=microsoft-azure&logoColor=white" alt="Azure AI" />
  <img src="https://img.shields.io/badge/scikit_learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white" alt="scikit-learn" />
  <img src="https://img.shields.io/badge/uv-AE15CE?style=for-the-badge&logo=python&logoColor=white" alt="uv" />
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker" />
  <img src="https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=JSON%20web%20tokens" alt="JWT" />
</div>

# HR-Pulse Backend API

> Le moteur intelligent de HR-Pulse, exploitant l'IA Azure et le Machine Learning pour l'analyse du marché de l'emploi.

## Table des matières
1. [Fonctionnalités Principales](#fonctionnalités-principales)
2. [Stack Technique Détaillée](#stack-technique-détaillée)
3. [Prérequis](#prérequis)
4. [Installation & Démarrage](#installation--démarrage)
5. [Structure du Projet](#structure-du-projet)
6. [Points de terminaison (Endpoints)](#-points-de-terminaison-endpoints)

---

## Fonctionnalités Principales

- **Authentification Sécurisée** : Inscription et connexion avec hachage de mot de passe (Argon2) et validation par jeton JWT.
- **Analyse NER (Azure AI)** : Extraction intelligente des compétences critiques à partir des offres d'emploi grâce au Named Entity Recognition.
- **Prédiction Salariale ML** : Modèle de régression (Scikit-learn) pour estimer le salaire moyen basé sur les compétences et l'intitulé du poste.
- **Répertoire SQL** : Recherche ultra-rapide parmi des milliers de titres de postes indexés dans Azure SQL.

## Stack Technique Détaillée

- **Framework** : [FastAPI](https://fastapi.tiangolo.com/) (Python 3.12+)
- **Gestionnaire de dépendances** : [uv](https://github.com/astral-sh/uv)
- **Base de données** : Azure SQL / MSSQL (via SQLAlchemy & PyODBC)
- **IA/ML** : 
  - Azure AI Language (Text Analytics)
  - Scikit-learn (Modèle prédictif)
- **Déploiement** : Docker / Docker Compose

## Prérequis

Avant de commencer, assurez-vous d'avoir installé :
- [Python 3.12+](https://www.python.org/downloads/)
- `uv` installé (`curl -LsSf https://astral.sh/uv/install.sh | sh`)
- [Docker](https://www.docker.com/) (Optionnel, pour le déploiement conteneurisé)

## Installation & Démarrage

### 1. Installation locale

```bash
# Cloner le dépôt et se placer dans le dossier backend
# git clone <votre-repo>
# cd HR-pulse-backend

# Synchroniser les dépendances avec uv
uv sync

# Configurer l'environnement
cp .env.example .env
# ⚠️ Remplissez le fichier .env avec vos clés Azure et vos accès SQL
```

### 2. Lancement

**En mode développement (local) :**
```bash
uv run uvicorn src.api.main:app --reload
```

**Avec Docker :**
```bash
docker build -t hr-pulse-backend .
docker run -p 8000:8000 hr-pulse-backend
```

## Structure du projet

```text
├── src/
│   ├── api/
│   │   ├── routers/   # Points de terminaison (Auth, Jobs, Predict)
│   │   ├── crud/      # Opérations sur la base de données
│   │   └── schemas/   # Modèles Pydantic (validation des données)
│   ├── core/          # Logique de sécurité et configuration système
│   └── database/      # Session SQLAlchemy et modèles de tables
├── ml_models_saved/   # Modèles Scikit-learn entraînés et exportés
├── data/              # Données brutes ou traitées (csv, etc.)
└── tests/             # Scripts de tests unitaires et d'intégration
```

## Points de terminaison (Endpoints)

| Méthode | Route | Description |
| :--- | :--- | :--- |
| `POST` | `/auth/register` | Création de compte utilisateur |
| `POST` | `/auth/login` | Authentification et génération de Token JWT |
| `GET`  | `/jobs/titles` | Liste tous les titres de postes disponibles |
| `GET`  | `/jobs/search` | Recherche par compétences (Extraction NER) |
| `POST` | `/predict/predict` | Prédiction salariale via IA ML |

---
**Documentation Interactive** : Une fois le serveur lancé, la documentation interactive Swagger complète est disponible sur : [http://localhost:8000/docs](http://localhost:8000/docs)
=======
# hr-pulse-backend
>>>>>>> origin/main
