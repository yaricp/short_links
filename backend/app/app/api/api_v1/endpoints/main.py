from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app import crud
from app.api import deps

router = APIRouter()


@router.get("/{short_text}")
def read_link(
    *,
    db: Session = Depends(deps.get_db),
    short_text: str,
) -> Any:
    """
    Gets link by short url and redirects to long url
    """
    link = crud.link.get_by_short_text(db=db, short_text=short_text)
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    return RedirectResponse(link.text)
