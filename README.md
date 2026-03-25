<div align="center">
  <img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi" alt="FastAPI" />
  <img src="https://img.shields.io/badge/Python_3.12-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Azure_SQL-0089D6?style=for-the-badge&logo=microsoft-azure&logoColor=white" alt="Azure SQL" />
  <img src="https://img.shields.io/badge/Azure_AI-0078D4?style=for-the-badge&logo=microsoft-azure&logoColor=white" alt="Azure AI" />
  <img src="https://img.shields.io/badge/scikit_learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white" alt="scikit-learn" />
  <img src="https://img.shields.io/badge/Jaeger-44C1D0?style=for-the-badge&logo=jaeger&logoColor=white" alt="Jaeger" />
  <img src="https://img.shields.io/badge/uv-AE15CE?style=for-the-badge&logo=python&logoColor=white" alt="uv" />
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker" />
  <img src="https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=JSON%20web%20tokens" alt="JWT" />
</div>

# HR-Pulse Backend API

Le moteur intelligent de **HR-Pulse**, conçu pour fournir une analyse avancée du marché de l'emploi grâce à l'Intelligence Artificielle et à l'apprentissage automatique (Machine Learning). Cette API robuste et performante sert au traitement des données RH, à l'extraction de compétences et à la prédiction salariale.

---

## 📑 Table des matières
1. [À propos du projet](#-à-propos-du-projet)
2. [Fonctionnalités Principales](#-fonctionnalités-principales)
3. [Stack Technique & Architecture](#-stack-technique--architecture)
4. [Prérequis](#-prérequis)
5. [Installation & Démarrage](#-installation--démarrage)
6. [Structure du Projet](#-structure-du-projet)
7. [Points de terminaison (Endpoints API)](#-points-de-terminaison-endpoints-api)

---

## 🚀 À propos du projet

L'application HR-Pulse Backend permet d'analyser les profils de candidats ou les offres d'emploi, en extrayant automatiquement les compétences clés via les services cloud d'Azure AI, et propose un modèle prédictif basé sur **Scikit-learn** pour estimer le salaire juste sur le marché en fonction de divers critères (intitulé du poste, compétences). Tout cela est supporté par une API asynchrone extrêmement rapide développée avec **FastAPI**.

## ✨ Fonctionnalités Principales

- **Authentification & Sécurité** : Système d'inscription et de connexion sécurisé avec hachage de mots de passe (**Argon2**) et protection des routes par jetons **JWT**.
- **Prédiction Salariale par Machine Learning** : Moteur d'inférence chargé dynamiquement (Scikit-learn) pour estimer le salaire moyen d'un profil métier.
- **Analyse Textuelle et NER (Azure AI)** : Extraction intelligente des entités nommées (NER) et des compétences à partir des offres d'emploi lors des processus d'ingénierie de données.
- **Base de données Cloud** : Interaction optimisée (via SQLAlchemy et PyODBC) avec une base de données distante **Azure SQL** regroupant des milliers de titres de postes indexés.
- **Observabilité et Tracing** : Intégration d'**OpenTelemetry** permettant le suivi et l'analyse de la performance des requêtes via **Jaeger**.

## 🛠 Stack Technique & Architecture

- **Backend Framework** : [FastAPI](https://fastapi.tiangolo.com/) (Python 3.12+)
- **Gestionnaire de dépendances ultra-rapide** : [uv](https://github.com/astral-sh/uv)
- **Base de données ORM** : SQLAlchemy 2.0 (Connecteur PyODBC)
- **Cloud & Base de données** : Azure SQL / MSSQL
- **Intelligence Artificielle & Data Science** : 
  - Azure AI Language (Text Analytics)
  - Scikit-learn (Modèle prédictif, Feature Engineering)
  - Pandas, NumPy
- **Monitoring & Tracing** : OpenTelemetry, Jaeger
- **Déploiement & Conteneurisation** : Docker, Docker Compose

## 📋 Prérequis

Avant de lancer le projet, assurez-vous d'avoir les éléments suivants installés sur votre machine :
- [Python 3.12+](https://www.python.org/downloads/)
- `uv` installé manuellement (`curl -LsSf https://astral.sh/uv/install.sh | sh`) ou via pip (`pip install uv`)
- un pilote [ODBC Driver for SQL Server](https://learn.microsoft.com/fr-fr/sql/connect/odbc/download-odbc-driver-for-sql-server) compatible avec votre OS.
- [Docker](https://www.docker.com/) & Docker Compose (si vous passez par un déploiement conteneurisé).

## Installation & Démarrage

### 1. Démarrage avec Docker (Recommandé)

Docker Compose s'occupe de monter l'API backend, le service Jaeger pour les traces de performance, ainsi que de lier le frontend si ce dernier est présent.

```bash
# Lancer l'environnement de développement complet (Backend + Jaeger)
docker-compose up --build
```
L'API sera accessible sur [http://localhost:8000](http://localhost:8000) et le tableau de bord des traces Jaeger sur [http://localhost:16686](http://localhost:16686).

### 2. Démarrage en mode Local (Développement)

Si vous préférez faire tourner le projet hors conteneur :

```bash
# Cloner le dépôt et se placer dans le dossier backend
git clone https://github.com/khadija199904/HR-Pulse-Backend.git
cd HR-pulse-backend

# Synchroniser l'environnement et installer les dépendances avec uv
uv sync

# Configurer les variables d'environnement
cp .env.example .env
```
> [!IMPORTANT]
> **Configuration requise** : Éditez le fichier `.env` pour y renseigner les URL d'accès à la base de données (`AZURE_DB_URL`), vos identifiants à l'API Azure AI (`AZURE_AI_KEY`, `AZURE_AI_ENDPOINT`), ainsi que la clé de signature JWT (`SECRET_KEY`).

```bash
# Lancer le serveur backend en mode auto-reload
uv run uvicorn src.api.main:app --reload
```

## 📂 Structure du projet

```text
├── src/
│   ├── ai/            # Scripts d'extraction NER et modèles ML
│   ├── api/
│   │   ├── routers/   # Contrôleurs API (Auth, Jobs, Predict)
│   │   ├── crud/      # Accès et manipulation de la BDD Azure SQL
│   │   ├── schemas/   # Modèles (Pydantic) assurant la validation i/o
│   │   └── services/  # Services logiques (ML inference, etc.)
│   ├── core/          # Configuration de sécurité, JWT, et Tracing
│   ├── data_engineering/ # Scripts d'ingestion massive DB (Azure SQL)
│   └── database/      # Connexion et déclaration des ORM (Models SQLAlchemy)
├── ml_models_saved/   # Modèles pré-entrainés Scikit-learn (ex: .pkl)
├── data/              # Données csv & artifacts
├── tests/             # Tests unitaires et d'intégration (pytest)
├── docker-compose.yml # Fichier de composition orchestrant backend, frontend, jaeger
└── pyproject.toml     # Configuration du projet et définition des dépendances (uv)
```

##  Infrastructure as Code (Terraform)

Le projet intègre une configuration **Terraform** simple et efficace pour provisionner l'environnement backend (Base de données) de manière reproductible sur Microsoft Azure.

- **Base de données Azure SQL** : Déploiement automatisé d'une base de données Azure SQL (`db-khadija`) rattachée à un serveur pré-existant réservé à la formation.

- **Déploiement** : 
  ```bash
  cd Terraform
  terraform init
  terraform apply
  ```

##  Points de terminaison (Endpoints API)

Les principales routes disponibles dans l'application :

| HTTP Method | Route | Catégorie | Description |
| :--- | :--- | :--- | :--- |
| `POST` | `/auth/register` | **Auth** | Création d'un nouveau compte utilisateur |
| `POST` | `/auth/login` | **Auth** | Connexion et génération d'un Token d'accès (JWT) |
| `GET`  | `/auth/profil` | **Auth** | Récupération du profil actuel (Protégé par JWT) |
| `GET`  | `/jobs/titles` | **Jobs** | Liste complète des intitulés de postes supportés |
| `GET`  | `/jobs/search` | **Jobs** | Recherche d'offres via les compétences (Skill filters) |
| `POST` | `/predict/predict`| **Predict** | Prédiction de la fourchette salariale pour un profil type |

---
 **Documentation Interactive (Swagger UI)** : Une fois le projet démarré, ne manquez pas de consulter la documentation native autogénérée par FastAPI : [http://localhost:8000/docs](http://localhost:8000/docs) (Redocs disponible sur `/redoc`).
