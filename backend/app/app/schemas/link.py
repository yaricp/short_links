from datetime import datetime
from typing import Optional

from pydantic import AnyUrl, BaseModel, FutureDate


# Shared properties
class LinkBase(BaseModel):
    text: Optional[AnyUrl] = None
    short_text: Optional[str] = None
    expired: Optional[datetime] = None


# Properties to receive on link creation
class LinkCreate(BaseModel):
    text: AnyUrl


# Properties to receive on link creation
class LinkCreateDB(BaseModel):
    text: AnyUrl
    short_text: str
    expired: FutureDate


# Properties to receive on link update
class LinkUpdate(LinkBase):
    pass


# Properties shared by models stored in DB
class LinkInDBBase(LinkBase):
    id: int
    text: AnyUrl
    short_text: str
    expired: datetime
    owner_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Link(LinkInDBBase):
    pass


# Properties properties stored in DB
class LinkInDB(LinkInDBBase):
    pass
