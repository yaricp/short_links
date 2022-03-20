"""
Module defines function for create short links
and for remove when expired ones
"""

from datetime import datetime, timedelta

from fastapi import Depends
from hashids import Hashids

from app import crud, schemas
from app.api import deps
from app.core.config import settings


def make_short_link(link: schemas.LinkCreate) -> schemas.LinkCreateDB:
    """Create short text from long url by using hashids library"""

    hashids = Hashids(salt=link.text)
    short_text = hashids.encode(123456)
    link_out = schemas.LinkCreateDB(
        text = link.text,
        short_text = short_text,
        expired = datetime.utcnow() + timedelta(
            minutes=settings.SHORT_LINK_EXPIRE_MINUTES
        )
    )
    return link_out


def remove_expired_links() -> None:
    """Removes all link objects with expired datetime"""
    crud.link.remove_expired(db=Depends(deps.get_db))
