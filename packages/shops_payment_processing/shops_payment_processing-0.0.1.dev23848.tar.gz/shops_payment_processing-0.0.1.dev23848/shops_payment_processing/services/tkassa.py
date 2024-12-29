import hashlib
import httpx

from fastapi import HTTPException
from shops_payment_processing.logging_config import logger
from shops_payment_processing.models.order import OrderResponseModel


class TKassaAPI:
    def __init__(self, terminal_id: str, terminal_password: str):
        self.terminal_id = terminal_id
        self.terminal_password = terminal_password
        self.url = "https://securepay.tinkoff.ru/v2"


    async def create_sbp_invoice(self, shop_name: str, order: OrderResponseModel, redirect_url: str):
        value = int(order.basket.amount * 100)

        customer_phone = order.user_contact_number if order.user_contact_number else None

        order_id = order.id

        # Build receipt items
        receipt_items = []
        for product in order.basket.products:
            item = {
                "Name": product.name,
                "Price": int(product.final_price * 100),
                "Quantity": product.count_in_basket,
                "Amount": int(product.final_price * 100) * product.count_in_basket,
                "PaymentMethod": "full_payment", # Adjust if payment method varies
                "PaymentObject": "commodity", # Adjust if payment object varies
                "Tax": "none" # Replace with actual tax if needed
            }
            receipt_items.append(item)

        # Build token generation values array
        token_gen_array = [("TerminalKey", self.terminal_id),
                           ("Amount", str(value)),
                            ("OrderId", order_id),
                            ("Description", f"Заказ {order.order_number}"),
                            ("SuccessURL", redirect_url),
                            ("FailURL", redirect_url),
                            ("Password", self.terminal_password)]

        # Sort array
        sorted_token_data = sorted(token_gen_array, key=lambda x: x[0])

        # Build token source string
        concatenated_values = ''.join(str(value) for key, value in sorted_token_data)

        #Build token
        token = hashlib.sha256(concatenated_values.encode('utf-8')).hexdigest()


        request_body = {
            "TerminalKey": self.terminal_id,
            "Amount": value,
            "OrderId": order_id,
            "Description": f"Заказ {order.order_number}",
            "Token": token,
            "DATA":{
                "orderId": order.id,
                "orderNumber": order.order_number
            },
            "SuccessURL": redirect_url,
            "FailURL": redirect_url,
            "Receipt": {
                "Items": receipt_items,
                "Taxation": "osn" # Replace with actual taxation if needed
            }
        }

        if customer_phone:
            request_body["Receipt"]["Phone"] = customer_phone # type: ignore
        else:
            request_body["Receipt"]["Email"] = "info@tg-shops.com" # type: ignore

        headers = {
            "Content-Type": "application/json"
        }

        async with httpx.AsyncClient() as client:
            logger.info(f"Creating Tkassa payment for order {order.id}")
            response = await client.post(
                url=f"{self.url}/Init",
                json=request_body,
                headers=headers,
            )
            if not response.status_code == 200:
                raise HTTPException(status_code=response.status_code, detail=response.text)
            return response.json()

