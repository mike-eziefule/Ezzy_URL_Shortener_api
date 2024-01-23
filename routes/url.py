"""Routes related to URL adding and listing."""
import validators
from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
import schemas
from utils import crud
from database import get_db
from utils.errors import raise_bad_request, raise_not_found
from routes import admin

router = APIRouter(tags=["URL Functionality"])

@router.get("/list", response_model=schemas.URLList)
async def list_urls(db: Session = Depends(get_db)):
    """Return a list of all URLs in the database."""
    url_list = [crud.get_list_info(item) for item in crud.get_all_urls(db=db)]
    return {"urls": url_list}


@router.post("/url", response_model=schemas.URLInfo)
async def create_url(url: schemas.URLBase, db: Session = Depends(get_db)):
    """Create a URL shortener entry."""
    if not validators.url(url.target_url):
        raise_bad_request(message="Your provided URL is not Valid")
    db_url = crud.create_db_url(db=db, url=url)
    return crud.get_admin_info(db_url)


@router.get("/{url_key}/peek", response_model=schemas.URL)
async def show_target_url(
    url_key: str, request: Request, db: Session = Depends(get_db)
):
    """
    Return only the target URL, do not redirect.

    This allows users to check the URL before visiting.
    """
    if db_url := crud.get_db_url_by_key(db=db, url_key=url_key):
        return db_url
    else:
        raise_not_found(request)


@router.get("/{url_key}")
async def forward_to_target_url(
    url_key: str, request: Request, db: Session = Depends(get_db)
):
    """Forward to the correct full URL."""
    if db_url := crud.get_db_url_by_key(db=db, url_key=url_key):
        crud.update_db_clicks(db=db, db_url=db_url)
        print(db_url.target_url)
        return RedirectResponse(db_url.target_url)
    else:
        raise_not_found(request)
