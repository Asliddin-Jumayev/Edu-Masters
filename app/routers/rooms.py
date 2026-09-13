from fastapi import APIRouter, status
from sqlalchemy import select
from app.database.base import MyDb
from app.models.branches import Branch
from app.models.rooms import Room
from app.schemes.rooms import RoomCreate, RoomResponse, RoomUpdate
from app.utils.checked import check_ident

router = APIRouter(tags=['Room'], prefix="/rooms")


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_room(room: RoomCreate, db: MyDb):

    # check branch id
    await check_ident(db, Branch, room.branch_id)

    obj = Room(
        **room.model_dump()
    )
    db.add(obj)
    await db.commit()
    return {"msg": "Room created successfully"}


@router.get('/', response_model=list[RoomResponse])
async def list_rooms(db: MyDb, is_active: bool = True):
    result = await db.execute(select(Room))

    if is_active:
        result = await db.execute(select(Room).where(Room.is_active == is_active))

    return result.scalars().all()


@router.put('/{room_id}')
async def update_room(room_id: int, room_data: RoomUpdate, db: MyDb):
    room = await check_ident(db, Room, room_id)

    if room.branch_id != room_data.branch_id:
        await check_ident(db, Branch, room_data.branch_id)

    room.name = room_data.name
    room.branch_id = room_data.branch_id
    room.capacity = room_data.capacity

    await db.commit()
    await db.refresh(room)
    return {"Msg": "Room edited successfully"}

@router.delete('/{room_id}')
async def delete_room(room_id: int, db: MyDb):

    room = await check_ident(db, Room, room_id)

    # soft delete
    room.is_active = False

    await db.commit()
    return {"msg": "Room soft delete"}
