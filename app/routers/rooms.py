from fastapi import APIRouter, status
from sqlalchemy import select
from app.database.base import MyDb
from app.models.branches import Branch
from app.models.rooms import Room
from app.schemas.rooms import RoomCreate, RoomResponse
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



@router.delete('/{room_id}')
async def delete_room(room_id: int, db: MyDb):

    room = await check_ident(db, Room, room_id)

    # soft delete
    room.is_active = False

    await db.commit()
    return {"msg": "Room soft deleted successfully"}
