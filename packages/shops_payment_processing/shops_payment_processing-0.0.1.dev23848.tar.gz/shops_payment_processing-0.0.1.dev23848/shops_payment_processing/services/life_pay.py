import httpx
from shops_payment_processing.logging_config import logger
from shops_payment_processing.models.order import UserBasketResponseModel
from shops_payment_processing.models.order import OrderResponseModel

def configure_description(basket: UserBasketResponseModel):
    """
    Configure description for sbp order in format: "1. Капучино 150мл x 1.0 = 3.00"
    """
    description = ""
    count = 1
    for product in basket.products:
        description += \
            f"{count}. {product.name} x {round(product.count_in_basket, 1)} = {round(product.count_in_basket * product.final_price, 2)}\n"
        count += 1
    return description


class LifePayAPI:

    def __init__(self, callback_base_url: str):
        self.url = 'https://api.life-pay.ru/v1'
        self.http_client = httpx.AsyncClient()
        self.CALLBACK_BASE_URL = callback_base_url

    async def create_sbp_invoice(self,
                                 shop_name: str,
                                 login: str,
                                 api_key: str,
                                 order: OrderResponseModel):
        extra_data = {}
        if order.user_contact_number:
            extra_data['customer_phone'] = order.user_contact_number.replace("+", "")
        async with self.http_client as client:
            payload = {
                "apikey": api_key,
                "login": login,
                "amount": order.basket.amount,
                "description": configure_description(order.basket),
                "currency": "RUB",
                "callback_url": f"{self.CALLBACK_BASE_URL}/{shop_name}/events/",
                **extra_data
            }
            logger.debug(f"Creating SBP invoice for order {order.id} {login} {api_key[:3]}")
            return await client.post(self.url + "/bill", json=payload)

    async def get_invoice_status(self, login: str, api_key: str, invoice_id: str):
        async with self.http_client as client:
            url = "https://api.life-pay.ru/v1/bill"
            payload = {
                "apikey": "93cd8d0e9.....",
                "login": "79114983065",
                "amount": "1.00",
                "description": "1. Капучино 150мл x 1.0 = 3.00",
                "customer_phone": "79009732993",
                "currency": "RUB",
                "customer_email": "pavel@tg-shops.com",
                "callback_url": "http://195.179.193.180:4889/webhook",
                "number": "11112222"
            }

            response = httpx.post(url, json=payload)

            print(response.text)
