from enum import Enum
from typing import Annotated

from annotated_types import Ge
from pydantic import BaseModel, field_validator, Field
from pydantic_core.core_schema import ValidationInfo
from typing_extensions import Doc


class PaymentTypes(str, Enum):
    manual_payment_request = "ManualPaymentRequest"
    external_card_payment_provider = "ExternalCardPaymentProvider"
    crypto_ton = "CryptoTON"
    xtr = "XTR"
    life_pay = "LifePay"
    yookassa = "yookassa"
    tkassa = "tkassa"


class DBProductInBasketV2(BaseModel):
    id: str  # product ID
    unique_id: str  # unique product ID in the basket, used it for product deleting
    extra_option_ids: list[str] = []

class MetaBaseModel(BaseModel):
    metadata: dict = Field(default_factory=dict, exclude=True)

class BaseProductResponseModel(MetaBaseModel):
    id: str
    name: str
    description: str = ""
    price: float
    final_price: float = 0
    currency: str
    preview_url: list[str] = []
    stock_qty: int
    orders_qty: int = 0

    @field_validator("final_price", mode="before")
    def set_final_price(cls, value, values: ValidationInfo):
        if not value:
            return values.data.get("price")
        return value

class ProductsInBasket(BaseProductResponseModel):
    count_in_basket: int = 1

class UserBasketResponseModel(BaseModel):
    id: str | None = None
    user_id: str | None = None
    order_id: str | None = None
    products_id: list[DBProductInBasketV2] = []
    coupon: str | None = None
    coupon_discount: Annotated[float, Doc("The amount of discount from attached coupon, if any.")] = 0
    amount: Annotated[float, Ge(0)] = 0  # this amount already includes discount
    preview_url: str = ""
    products: list[ProductsInBasket] = []


class OrderResponseModel(UserBasketResponseModel):
    id: str
    basket: UserBasketResponseModel
    user_id: str | None = None
    basket_id: str | None = None
    status: str | None = None
    order_number: str = "#0001"
    process_key: int | None = None
    coupon: str | None = None
    user_contact_number:str | None = None