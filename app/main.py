from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from routers.auth import auth_router
from routers.task import task_router
from routers.employee import employee_router
from routers.health import health_router
from database import BaseSQL, engine
from fastapi import FastAPI
from fastapi.security import HTTPBearer




@asynccontextmanager
async def lifespan(app: FastAPI):
    BaseSQL.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="My title",
    description="My description",
    version="0.0.1",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permet toutes les origines. Pour la production, précise les URLs de ton frontend.
    allow_credentials=True,
    allow_methods=["*"],  # Permet toutes les méthodes HTTP
    allow_headers=["*"],  # Permet tous les headers
)

bearer_scheme = HTTPBearer()


app.include_router(task_router)
app.include_router(employee_router)
app.include_router(auth_router)
app.include_router(health_router)
