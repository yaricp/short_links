from typing import Optional

from sqlalchemy.orm import Session

from app import crud, models
from app.schemas.link import LinkCreate
from app.services import make_short_link
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_lower_string


def create_random_link(db: Session, *, owner_id: Optional[int] = None) -> models.Link:
    if owner_id is None:
        user = create_random_user(db)
        owner_id = user.id
    text = "http://%s" % random_lower_string()
    item_in = LinkCreate(text=text)
    item_for_db = make_short_link(item_in)
    return crud.link.create_with_owner(db=db, obj_in=item_for_db, owner_id=owner_id)
