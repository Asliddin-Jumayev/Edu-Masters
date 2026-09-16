from fastapi import FastAPI
from app.routers.branches import router as branches_router
from app.routers.rooms import router as rooms_router
from app.routers.employees import router as employees_router
from app.routers.auth import router as auth_router

app = FastAPI(title="Edu Masters system API", version="1.0", docs_url='/')

app.include_router(auth_router)
app.include_router(branches_router)
app.include_router(rooms_router)
app.include_router(employees_router)