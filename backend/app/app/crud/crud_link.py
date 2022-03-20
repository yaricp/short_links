from datetime import datetime
from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import delete
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.link import Link
from app.schemas.link import LinkCreateDB, LinkUpdate


class CRUDLink(CRUDBase[Link, LinkCreateDB, LinkUpdate]):
    """CRUD for Link model"""

    def get_by_text(self, db: Session, *, text: str) -> Optional[Link]:
        """Gets link by full text from db"""
        return db.query(Link).filter(Link.text == text).first()

    def get_by_short_text(self, db: Session, *, short_text: str) -> Optional[Link]:
        """Gets link by short text from db"""
        return db.query(Link).filter(Link.short_text == short_text).first()

    def create_with_owner(
        self, db: Session, *, obj_in: LinkCreateDB, owner_id: int
    ) -> Link:
        """Creates new short link in db"""
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, owner_id=owner_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_owner(
        self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[Link]:
        """Gets all links from db by owner"""
        return (
            db.query(self.model)
            .filter(Link.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def remove_expired(self, db: Session) -> None:
        """Removes all links with expired datetime"""
        statement = delete(Link).where(Link.expired < datetime.utcnow())
        db.execute(statement=statement)


link = CRUDLink(Link)
