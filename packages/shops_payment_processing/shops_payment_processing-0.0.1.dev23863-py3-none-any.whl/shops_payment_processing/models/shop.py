from pydantic import BaseModel


class ShopDetailsModel(BaseModel):
    shop_id: str
    shop_name: str
    friendly_name: str
    shop_language: str = "RU"
    contact_phone: str | None = None
    contact_email: str