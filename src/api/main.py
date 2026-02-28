from fastapi import FastAPI
from src.api.routers import auth, predict, jobs
from src.database.session import Base, engine
from src.core.tracing import setup_tracing

app = FastAPI(title="HR Pulse Application")

# Initialize OpenTelemetry Tracing
setup_tracing(app)

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(predict.router)
app.include_router(jobs.router)
