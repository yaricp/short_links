from typing import TYPE_CHECKING

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .user import User  # noqa: F401


class Link(Base):
    """Model for link objects in db"""
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, index=True)
    short_text = Column(String, index=True, nullable=True)
    expired = Column(DateTime)
    owner_id = Column(Integer, ForeignKey("user.id"))
    owner = relationship("User", back_populates="links")
