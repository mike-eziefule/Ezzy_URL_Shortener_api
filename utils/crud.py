"""CRUD operations."""
from sqlalchemy.orm import Session
from config import get_settings
from starlette.datastructures import URL
from utils import random
import models, schemas
from config import get_settings

def get_list_info(db_url: models.URL) -> schemas.URLListItem:
    """Return List info for the URL."""
    base_url = URL(get_settings().base_url)
    db_url.url = str(base_url.replace(path=db_url.key))
    return db_url


def get_admin_info(db_url: models.URL) -> schemas.URLInfo:
    """Return the Admin info."""
    base_url = URL(get_settings().base_url)
    db_url.url = str(base_url.replace(path=db_url.key))
    return db_url


def create_db_url(db: Session, url: schemas.URLBase) -> models.URL:
    """Create URL in the Database."""
    key = random.create_unique_random_key(db)
    secret_key = f"{key}_{random.create_random_key(length=8)}"
    db_url = models.URL(
        target_url=url.target_url,
        key=key,
        private_key=secret_key,
    )
    db.add(db_url)
    db.commit()
    db.refresh(db_url)

    return db_url


def update_db_url(
    db: Session, url: schemas.URLBase, new_url: schemas.URLBase
) -> models.URL:
    """Update URL entry with new target."""
    url.target_url = new_url.target_url
    db.commit()
    db.refresh(url)
    return url


def get_all_urls(db: Session):
    """Return a list of all URL's."""
    return db.query(models.URL).all()


def get_db_url_by_key(db: Session, url_key: str) -> models.URL:
    """Return a URL by specified key."""
    return (
        db.query(models.URL)
        .filter(models.URL.key == url_key, models.URL.is_active == True)
        .first()
    )


def get_db_url_by_private_key(db: Session, private_key: str) -> models.URL:
    """Return a URL by the Secret key."""
    return (
        db.query(models.URL).filter(models.URL.private_key == private_key).first()
    )


def update_db_clicks(db: Session, db_url: schemas.URL) -> models.URL:
    """Update the count of times the link has been visited."""
    db_url.clicks += 1
    db.commit()
    db.refresh(db_url)
    return db_url


def delete_db_url_by_private_key(db: Session, private_key: str) -> models.URL:
    """Delete an existing URL."""
    
    db_url = get_db_url_by_private_key(db, private_key)
    
    return db_url

