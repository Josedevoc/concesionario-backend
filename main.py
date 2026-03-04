from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import database
from app.routers import vehicles
from app.routers import auth

app = FastAPI(title="Concesionario API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

app.include_router(auth.router)
app.include_router(vehicles.router)

@app.get("/")
async def root():
    return {"message": "Concesionario API corriendo"}