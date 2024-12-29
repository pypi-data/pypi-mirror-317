from fastapi import HTTPException

from shops_payment_processing.logging_config import logger

from shops_payment_processing.models.payment import PaymentMethodDBResponseModel
from shops_payment_processing.models.invoice import InvoiceWithPaymentLinkMessageModel
from shops_payment_processing.models.order import PaymentTypes, OrderResponseModel
from shops_payment_processing.models.shop import ShopDetailsModel
from shops_payment_processing.models.user import UserModel
from shops_payment_processing.services.life_pay import LifePayAPI
from shops_payment_processing.services.tkassa import TKassaAPI
from shops_payment_processing.services.yookassa import YooKassaAPI
from shops_payment_processing.utils.link_generation import generate_web_app_order_link


class InvoiceCreation:
    def __init__(self, base_redirect_url: str, base_callback_url: str):
        self.BASE_REDIRECT_URL = base_redirect_url
        self.BASE_CALLBACK_URL = base_callback_url

    async def get_life_pay_sbp_payment_data(
        self,
        user: UserModel,
        order: OrderResponseModel,
        payment: PaymentMethodDBResponseModel,
        shop_details: ShopDetailsModel
    ) -> InvoiceWithPaymentLinkMessageModel:
        fiat_currency = order.basket.products[0].currency
        if fiat_currency != "RUB":
            raise HTTPException(status_code=404, detail="LifePay payment method is only available for RUB currency")

        login = ""
        if payment.meta:
            for meta in payment.meta:
                if meta.key == "LIFE_PAY_LOGIN" and meta.value:
                    login = meta.value[0]
                    break
        if not login or not payment.payment_data:
            raise HTTPException(status_code=404, detail="LifePay login was not configured for the shop")
        life_pay_connector = LifePayAPI(callback_base_url=self.BASE_CALLBACK_URL)
        invoice_response = await life_pay_connector.create_sbp_invoice(
            shop_name=shop_details.shop_name,
            api_key=payment.payment_data,
            login=login,
            order=order)
        if invoice_response.status_code != 200:
            raise HTTPException(status_code=500, detail="Error creating LifePay invoice: " + invoice_response.text)
        invoice_json = invoice_response.json()
        invoice_data = invoice_json.get("data")
        if not invoice_data:
            invoice_error_message = invoice_json.get("message")
            if invoice_error_message:
                raise HTTPException(status_code=500, detail=invoice_error_message)
            raise HTTPException(status_code=500, detail="Error creating LifePay invoice: " + invoice_response.text)

        logger.debug(f"LifePay SBP invoice data: {invoice_data}")
        payment_url = invoice_data.get("paymentUrlWeb")
        number = invoice_data.get("number")
        qr_url = invoice_data.get("paymentUrl")
        if not payment_url or not number or not qr_url:
            raise HTTPException(status_code=500, detail="Missing data from LifePay: " + invoice_response.text)
        return InvoiceWithPaymentLinkMessageModel(
            chat_id=user.tg_id,
            order_id=order.id,
            order_number=order.order_number,
            payload=number,
            currency=fiat_currency,
            payment_address=qr_url,
            payment_link=payment_url,
            amount=order.basket.amount
        )



    async def get_yookassa_payment_data(
        self,
        user: UserModel,
        order: OrderResponseModel,
        payment: PaymentMethodDBResponseModel,
        shop_details: ShopDetailsModel
    ) -> InvoiceWithPaymentLinkMessageModel:
        fiat_currency = order.basket.products[0].currency
        if fiat_currency != "RUB":
            raise HTTPException(status_code=404, detail="Yookassa payment method is only available for RUB currency")

        account_id = ""
        if payment.meta:
            for meta in payment.meta:
                if meta.key == "YOOKASSA_ACCOUNT_ID" and meta.value:
                    account_id = meta.value[0]
                    break
        if not account_id or not payment.payment_data:
            raise HTTPException(status_code=404, detail="YooKassa login was not configured for the shop")
        yookassa_connector = YooKassaAPI(
            account_id, payment.payment_data
        )
        invoice_json = await yookassa_connector.create_sbp_invoice(
            shop_name=shop_details.shop_name,
            order=order,
            redirect_url=generate_web_app_order_link(shop_name=shop_details.shop_name, order_id=order.id, tg_web_app_url=self.BASE_REDIRECT_URL))
        invoice_data = invoice_json.get("confirmation", {})
        if not invoice_data:
            invoice_error_message = invoice_json.get("description")
            if invoice_error_message:
                raise HTTPException(status_code=500, detail=invoice_error_message)
            raise HTTPException(status_code=500, detail=f"YooKassa: {invoice_data}")

        logger.debug(f"YooKassa SBP invoice data: {invoice_data}")
        payment_url = invoice_data.get("confirmation_url")
        number = invoice_json.get("id")
        qr_url = invoice_data.get("confirmation_url")
        if not payment_url or not number or not qr_url:
            raise HTTPException(status_code=500, detail=f"YooKassa: {invoice_data}")
        return InvoiceWithPaymentLinkMessageModel(
            chat_id=user.tg_id,
            order_id=order.id,
            order_number=order.order_number,
            payload=number,
            currency=fiat_currency,
            payment_address=qr_url,
            payment_link=payment_url,
            amount=order.basket.amount
        )


    async def get_tkassa_payment_data(
        self,
        user: UserModel,
        order: OrderResponseModel,
        payment: PaymentMethodDBResponseModel,
        shop_details: ShopDetailsModel
    ) -> InvoiceWithPaymentLinkMessageModel:
        fiat_currency = order.basket.products[0].currency
        if fiat_currency != "RUB":
            raise HTTPException(status_code=404, detail="Tkassa payment method is only available for RUB currency")

        terminal_id = ""
        if payment.meta:
            for meta in payment.meta:
                if meta.key == "TKASSA_TERMINAL_ID" and meta.value:
                    terminal_id = meta.value[0]
                    break
        if not terminal_id or not payment.payment_data:
            raise HTTPException(status_code=404, detail="Tkassa credentials was not configured for the shop")
        tkassa_connector = TKassaAPI(
            terminal_id=terminal_id,
            terminal_password=payment.payment_data
        )
        invoice_json = await tkassa_connector.create_sbp_invoice(
            shop_name=shop_details.shop_name,
            order=order,
            redirect_url=generate_web_app_order_link(shop_name=shop_details.shop_name, order_id=order.id, tg_web_app_url=self.BASE_REDIRECT_URL))
        if not invoice_json.get("Success"):
            invoice_error_message = invoice_json.get("Message")
            invoice_error_details = invoice_json.get("Details")
            if invoice_error_message:
                invoice_error_response_message: str = invoice_error_message
                if invoice_error_details:
                    invoice_error_response_message = invoice_error_response_message + " : " + invoice_error_details
                raise HTTPException(status_code=500, detail=invoice_error_response_message)
            raise HTTPException(status_code=500, detail=f"Tkassa: {invoice_json}")

        logger.debug(f"Tkassa SBP invoice data: {invoice_json}")
        payment_url = invoice_json.get("PaymentURL")
        number = invoice_json.get("PaymentId")
        qr_url = invoice_json.get("PaymentURL")
        if not payment_url or not number or not qr_url:
            raise HTTPException(status_code=500, detail=f"Tkassa: {invoice_json}")
        return InvoiceWithPaymentLinkMessageModel(
            chat_id=user.tg_id,
            order_id=order.id,
            order_number=order.order_number,
            payload=number,
            currency=fiat_currency,
            payment_address=qr_url,
            payment_link=payment_url,
            amount=order.basket.amount
        )



    async def get_invoice_data(
            self,
            payment_type: PaymentTypes,
            user: UserModel,
            order: OrderResponseModel,
            shop_details: ShopDetailsModel
    ) -> InvoiceWithPaymentLinkMessageModel | None:
        invoice_data = None
        if payment_type == PaymentTypes.life_pay.value:
            invoice_data = await self.get_life_pay_sbp_payment_data(
                user=user, order=order, payment=payment_type, shop_details=shop_details
            )

        elif payment_type == PaymentTypes.yookassa.value:
            invoice_data = await self.get_yookassa_payment_data(
                user=user, order=order, payment=payment_type, shop_details=shop_details
            )

        elif payment_type == PaymentTypes.tkassa.value:
            invoice_data = await self.get_tkassa_payment_data(
                user=user, order=order, payment=payment_type, shop_details=shop_details
            )

        return invoice_data