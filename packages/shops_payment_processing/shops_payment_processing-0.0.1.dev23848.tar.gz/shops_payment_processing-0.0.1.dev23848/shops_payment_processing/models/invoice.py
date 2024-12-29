from pydantic import BaseModel


class InvoiceBaseModel(BaseModel):
    chat_id: int
    order_id: str
    order_number: str  # order_number
    payload: str  # can be used for subscription for update
    amount: float
    currency: str
    payment_address: str
    payment_timeout: int | None = None


class InvoiceWithPaymentLinkMessageModel(InvoiceBaseModel):
    payment_link: str