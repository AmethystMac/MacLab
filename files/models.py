from pydantic import BaseModel, Field

class User(BaseModel):
    name: str = Field(min_length=1, max_length=40)
    age: int = Field(ge=0, le=150)
    sex: str = Field(max_length=6)
