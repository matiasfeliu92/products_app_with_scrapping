from pydantic import BaseModel, field_validator, HttpUrl
from fastapi import HTTPException

from src.config.scrapper_settings import ScrapperSettings

scrapper_settings = ScrapperSettings()
stores = scrapper_settings.STORES

class ProductInput(BaseModel):
    link: HttpUrl

    @field_validator("link")
    @classmethod
    def validate_if_link_is_not_empty(cls, v: HttpUrl):
        if not v:
            raise ValueError("link is not valid, you must give a valid url")
        return v

    @field_validator("link")
    @classmethod
    def validate_store(cls, v: HttpUrl):
        if not any(store in v.host for store in stores):
            raise ValueError(
                f"Store link must be from {', '.join(stores)}"
            )
        return v