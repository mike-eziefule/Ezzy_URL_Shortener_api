"""Routes for Admin functionality."""
import validators
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
import schemas
from utils import crud
from database import get_db
from utils.errors import raise_bad_request, raise_not_found

router = APIRouter(tags=["Administration"], prefix="/admin")


@router.get("/{private_key}",name="administration info", response_model=schemas.URLInfo)
async def get_url_info(private_key: str, request: Request, db: Session = Depends(get_db)):
    """Admin path to return the URL info for a specific {private_key}."""
    if db_url := crud.get_db_url_by_secret_key(db, private_key=private_key):
        return crud.get_admin_info(db_url)
    else:
        raise_not_found(request)


@router.patch("/{private_key}", response_model=schemas.URL)
async def edit_url(
    new_url: schemas.URLBase,
    private_key: str,
    request: Request,
    db: Session = Depends(get_db),
):
    """Admin path to edit the URL link."""
    if not validators.url(new_url.target_url):
        raise_bad_request(message="Your provided URL is not Valid")
    if db_url := crud.get_db_url_by_private_key(db, private_key=private_key):
        return crud.update_db_url(db=db, url=db_url, new_url=new_url)
    else:
        raise_not_found(request)


@router.delete("/{private_key}")
async def delete_url(
    private_key: str, request: Request, db: Session = Depends(get_db)
):
    """Endpoint to delete (deactivate) a URL."""
    
    if db_url := crud.delete_db_url_by_private_key(db=db, private_key=private_key):
        
        if db_url:
            
            db.delete(db_url)
            db.commit()
            message = (
                f"Successfully deleted shortened URL"
            )
            return {"detail": message}
    else:
        raise_not_found(request)
