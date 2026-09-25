from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.branches import router as branches_router
from app.routers.rooms import router as rooms_router
from app.routers.employees import router as employees_router
from app.routers.auth import router as auth_router
from app.routers.roles import router as role_router
from app.routers.employee_roles import router as employee_roles_router
from app.utils.config import settings

app = FastAPI(title="Edu Masters system API", version="1.0", docs_url='/')

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(role_router)
app.include_router(employee_roles_router)
app.include_router(branches_router)
app.include_router(rooms_router)
app.include_router(employees_router)