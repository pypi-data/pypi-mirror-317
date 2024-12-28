import httpx
import random
from fastapi import HTTPException
from shops_payment_processing.logging_config import logger
from shops_payment_processing.models.order import OrderResponseModel

class YooKassaAPI:
    def __init__(self, account_id: str, secret_key: str):
        self.account_id = account_id
        self.secret_key = secret_key
        self.url = "https://api.yookassa.ru/v3"

    async def create_sbp_invoice(self, shop_name: str, order: OrderResponseModel, redirect_url: str):
        # Prepare the payment request body
        # value = round(order.basket.amount, 2)
        value = f"{round(order.basket.amount, 2):.2f}"
        currency = "RUB"
        # payment_description = configure_description(order.basket)
        customer_phone = order.user_contact_number.replace("+", "") if order.user_contact_number else None

        # Build receipt items
        receipt_items = []
        for product in order.basket.products:
            item = {
                "description": product.name,
                "quantity": f"{product.count_in_basket:.2f}",
                "amount": {
                    "value": f"{round(product.final_price):.2f}",
                    "currency": currency,
                },
                "vat_code": "2",  # Replace with the actual VAT code as needed
                "payment_mode": "full_payment",  # Adjust if payment mode varies
                "payment_subject": "commodity",  # Adjust if payment subject varies
                "country_of_origin_code": "RU"  # Assuming this exists
                # "product_code": product.id  # Assuming this exists # Use if goods marking needed
                # "customs_declaration_number": product.customs_declaration_number,  # Assuming this exists
                # "excise": f"{product.excise:.2f}" if hasattr(product, 'excise') else None,  # Optional
                # "supplier": {
                #     "name": product.supplier_name,  # Assuming this exists
                #     "phone": product.supplier_phone,  # Assuming this exists
                #     "inn": product.supplier_inn,  # Assuming this exists
                # },
            }
            receipt_items.append(item)

        # Build the request payload
        request_body = {
            "amount": {
                "value": value,
                "currency": currency,
            },
            "confirmation": {
                "type": "redirect",
                "return_url": redirect_url
            },
            "capture": True,
            "description": f"Заказ {order.order_number}",
            "metadata": {
                "orderId": order.id,
                "orderNumber": order.order_number
            },
            "receipt": {
                "items": receipt_items
            }
        }

        # Add customer phone if available
        if customer_phone:
            request_body["receipt"]["customer"] = {"phone": customer_phone} # type: ignore
        else:
            request_body["receipt"]["customer"] = {"email": "info@tg-shops.com"}  # type: ignore

        # Prepare authentication
        auth = httpx.BasicAuth(self.account_id, self.secret_key)

        # Set the Idempotence-Key header using the order ID
        headers = {
            "Idempotence-Key": f"{str(order.id)}:{random.randint(1000, 9999)}",
            "Content-Type": "application/json"
        }

        async with httpx.AsyncClient() as client:
            logger.info(f"Creating YooKassa payment for order {order.id}")
            response = await client.post(
                url=f"{self.url}/payments",
                auth=auth,
                json=request_body,
                headers=headers,
            )
            if not response.status_code == 200:
                raise HTTPException(status_code=response.status_code, detail=response.text)

            return response.json()