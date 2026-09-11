from pydantic import BaseModel, Field


class RoomBase(BaseModel):
    branch_id: int
    name: str
    capacity: int = Field(gt=0)


class RoomCreate(RoomBase):
    pass


class RoomUpdate(RoomBase):
    pass


class RoomResponse(BaseModel):
    id: int
    branch_id: int
    name: str
    capacity: int
    is_active: bool