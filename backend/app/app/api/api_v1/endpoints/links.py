from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas, services
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Link])
def read_links(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve links.
    """
    if crud.user.is_superuser(current_user):
        links = crud.link.get_multi(db, skip=skip, limit=limit)
    else:
        links = crud.link.get_multi_by_owner(
            db=db, owner_id=current_user.id, skip=skip, limit=limit
        )
    return links


@router.post("/", response_model=schemas.Link)
def create_link(
    *,
    db: Session = Depends(deps.get_db),
    item_in: schemas.LinkCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Test if link with text exists then return one.
    Create new link if not found.
    """
    link = crud.link.get_by_text(db=db, text=item_in.text)
    if link:
        return link
    item_to_db = services.make_short_link(item_in)
    link = crud.link.create_with_owner(
        db=db, obj_in=item_to_db, owner_id=current_user.id
    )
    return link


@router.put("/{id}", response_model=schemas.Link)
def update_link(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    item_in: schemas.LinkUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an link.
    """
    link = crud.link.get(db=db, id=id)
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    if not crud.user.is_superuser(current_user) and (link.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    link = crud.link.update(db=db, db_obj=link, obj_in=item_in)
    return link


@router.get("/{id}", response_model=schemas.Link)
def read_link(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get link by ID.
    """
    link = crud.link.get(db=db, id=id)
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    if not crud.user.is_superuser(current_user) and (link.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return link


@router.delete("/{id}", response_model=schemas.Link)
def delete_link(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an link.
    """
    link = crud.link.get(db=db, id=id)
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    if not crud.user.is_superuser(current_user) and (link.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    link = crud.link.remove(db=db, id=id)
    return link
