# HR-Pulse Backend API

## Description
Backend for the HR-Pulse project, implementing data ingestion, skills extraction via Azure AI, and salary prediction.

## Tech Stack
- **Framework**: FastAPI
- **AI**: Azure AI Language (NER)
- **ML**: Scikit-learn (Regression)
- **Data**: Azure SQL Database
- **Ops**: Docker, Terraform, CI/CD (GitHub Actions)

## Setup
1. Install [uv](https://github.com/astral-sh/uv).
2. Run `uv sync` to install dependencies.
3. Copy `.env.example` to `.env` and fill in the values.
4. Run locally: `uv run fastapi dev src/api/main.py`