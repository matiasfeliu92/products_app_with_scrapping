from pydantic import BaseModel

class CategoryOut(BaseModel):
    main: str
    sub: str