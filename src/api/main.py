from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.database.session import Base,engine
from src.api.routers import auth, predict, jobs
from src.core.tracing import setup_tracing

app = FastAPI(title="HR Pulse Application")

# Initialize OpenTelemetry Tracing
setup_tracing(app)

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3001",
    "http://192.168.1.195:3000",
    "http://192.168.1.195:3001",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(predict.router)
app.include_router(jobs.router)
