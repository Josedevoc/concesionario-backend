from fastapi import APIRouter, HTTPException
from app.database import database, vehicles_table
from app.schemas import VehicleCreate, VehicleUpdate, VehicleResponse
from typing import List

router = APIRouter(prefix="/api/vehicles", tags=["vehicles"])

@router.get("/", response_model=List[VehicleResponse])
async def get_all():
    query = vehicles_table.select().order_by(vehicles_table.c.created_at.desc())
    return await database.fetch_all(query)

@router.post("/", response_model=VehicleResponse, status_code=201)
async def create(vehicle: VehicleCreate):
    query = vehicles_table.insert().values(**vehicle.model_dump())
    vehicle_id = await database.execute(query)
    return await database.fetch_one(
        vehicles_table.select().where(vehicles_table.c.id == vehicle_id)
    )

@router.put("/{vehicle_id}", response_model=VehicleResponse)
async def update(vehicle_id: int, vehicle: VehicleUpdate):
    exists = await database.fetch_one(
        vehicles_table.select().where(vehicles_table.c.id == vehicle_id)
    )
    if not exists:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")
    query = vehicles_table.update().where(
        vehicles_table.c.id == vehicle_id
    ).values(**vehicle.model_dump())
    await database.execute(query)
    return await database.fetch_one(
        vehicles_table.select().where(vehicles_table.c.id == vehicle_id)
    )

@router.delete("/{vehicle_id}", status_code=204)
async def delete(vehicle_id: int):
    exists = await database.fetch_one(
        vehicles_table.select().where(vehicles_table.c.id == vehicle_id)
    )
    if not exists:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")
    await database.execute(
        vehicles_table.delete().where(vehicles_table.c.id == vehicle_id)
    )