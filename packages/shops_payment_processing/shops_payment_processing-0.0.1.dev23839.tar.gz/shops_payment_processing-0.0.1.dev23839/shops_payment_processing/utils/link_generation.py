import base64
import json


def generate_web_app_order_link(shop_name: str, order_id: str, tg_web_app_url: str) -> str:
    startapp_param = {"redirect": f"/{shop_name}/order/{order_id}"}
    startapp_param_json = json.dumps(startapp_param)
    startapp_param_base64 = base64.b64encode(startapp_param_json.encode()).decode()
    return f"{tg_web_app_url}?startapp={startapp_param_base64}"
