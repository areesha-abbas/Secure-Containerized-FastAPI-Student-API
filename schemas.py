from pydantic import BaseModel


class StudentCreate(BaseModel):
    name: str


class StudentResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True