import time
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app import crud
from app.schemas.link import LinkCreate, LinkUpdate
from app.services import make_short_link
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_lower_string


def test_create_link(db: Session) -> None:
    text = "http://%s" % random_lower_string()
    link_in = LinkCreate(text=text)
    link_for_db = make_short_link(link_in)
    user = create_random_user(db)
    link = crud.link.create_with_owner(db=db, obj_in=link_for_db, owner_id=user.id)
    assert link.text == text
    assert link.short_text == link_for_db.short_text
    assert link.owner_id == user.id


def test_get_link(db: Session) -> None:
    text = "http://%s" % random_lower_string()
    link_in = LinkCreate(text=text)
    link_for_db = make_short_link(link_in)
    user = create_random_user(db)
    link = crud.link.create_with_owner(db=db, obj_in=link_for_db, owner_id=user.id)
    stored_link = crud.link.get(db=db, id=link.id)
    assert stored_link
    assert link.id == stored_link.id
    assert link.text == stored_link.text
    assert link.short_text == stored_link.short_text
    assert link.expired == stored_link.expired
    assert link.owner_id == stored_link.owner_id


def test_get_link_by_short_url(db: Session) -> None:
    text = "http://%s" % random_lower_string()
    link_in = LinkCreate(text=text)
    link_for_db = make_short_link(link_in)
    user = create_random_user(db)
    link = crud.link.create_with_owner(db=db, obj_in=link_for_db, owner_id=user.id)
    stored_link = crud.link.get_by_short_text(db=db, short_text=link_for_db.short_text)
    assert stored_link
    assert link.id == stored_link.id
    assert link.text == stored_link.text
    assert link.short_text == stored_link.short_text
    assert link.expired == stored_link.expired
    assert link.owner_id == stored_link.owner_id


def test_update_link(db: Session) -> None:
    text = "http://%s" % random_lower_string()
    link_in = LinkCreate(text=text)
    link_for_db = make_short_link(link_in)
    user = create_random_user(db)
    link = crud.link.create_with_owner(db=db, obj_in=link_for_db, owner_id=user.id)
    short_text2 = "http://%s" % random_lower_string()
    link_update = LinkUpdate(short_text=short_text2)
    link2 = crud.link.update(db=db, db_obj=link, obj_in=link_update)
    assert link.id == link2.id
    assert link.text == link2.text
    assert link2.short_text == short_text2
    assert link.owner_id == link2.owner_id


def test_delete_link(db: Session) -> None:
    text = "http://%s" % random_lower_string()
    link_in = LinkCreate(text=text)
    link_for_db = make_short_link(link_in)
    user = create_random_user(db)
    link = crud.link.create_with_owner(db=db, obj_in=link_for_db, owner_id=user.id)
    link2 = crud.link.remove(db=db, id=link.id)
    link3 = crud.link.get(db=db, id=link.id)
    assert link3 is None
    assert link2.id == link.id
    assert link2.text == text
    assert link2.short_text == link_for_db.short_text
    assert link2.owner_id == user.id


def test_remove_expired_links(db: Session) -> None:
    text = "http://%s" % random_lower_string()
    link_in = LinkCreate(text=text)
    link_for_db = make_short_link(link_in)
    user = create_random_user(db)
    link = crud.link.create_with_owner(db=db, obj_in=link_for_db, owner_id=user.id)
    expired = datetime.utcnow() + timedelta(
            seconds=1
        )
    link_update = LinkUpdate(expired=expired)
    link2 = crud.link.update(db=db, db_obj=link, obj_in=link_update)
    assert link.id == link2.id
    assert link.text == link2.text
    assert link.owner_id == link2.owner_id
    time.sleep(2)
    crud.link.remove_expired(db=db)
    link3 = crud.link.get(db=db, id=link.id)
    assert link3 is None
