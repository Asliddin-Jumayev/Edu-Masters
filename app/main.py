from fastapi import FastAPI
from app.routers.branches import router as branches_router
from app.routers.rooms import router as rooms_router


app = FastAPI(title="ERP/CRM system API", version="1.0", docs_url='/')


app.include_router(branches_router)
app.include_router(rooms_router)