import json
import os
import random
import math
from django.core.cache import cache
import requests

# from datetime import timedelta

from rest_framework.views import exception_handler
from rest_framework.exceptions import Throttled
import datetime


TIMEOUT_IN_MINUTES = 3
WHATSAPP_API_URL = "https://graph.facebook.com/"


# TODO: make a correct digit based otp : DONE
def generate_otp_of_size(digits, serialized=None, phone_number=None):
    try:
        digit_range = "0123456789"
        otp = ""

        for _ in range(digits):
            otp += digit_range[math.floor(random.random() * 10)]

        # TODO: send sms
        print(otp)
        # print(serialized)
        print(phone_number)

        if serialized:
            user_data = {"serialized": serialized, "otp": otp}
            cache.set(
                f"{serialized.validated_data['phone_number']}",
                user_data,
                timeout=TIMEOUT_IN_MINUTES * 60,
            )
        else:
            print(phone_number)
            user_data = {"otp": otp}
            cache.set(f"{phone_number}", user_data, timeout=TIMEOUT_IN_MINUTES * 60)

            print(cache.get(f"{phone_number}"), "get cache")

        # if cache.get("8787867666"):
        #     print("Found in cache")
        # else:
        #     print("no such no. in cache")

    except Exception as e:
        print(e)
        return False
    # send sms
    return True


def set_expiration_date(exp_period):
    now_date = datetime.datetime.now()
    exp_date = now_date + datetime.timedelta(days=exp_period)
    print(exp_date)
    return exp_date


def send_whatsapp_confirmation(
    reciepient_phone_number, message_template_name, coupon_data
):
    phone_id = os.environ.get("WHATSAPP_PHONE_NUMBER_ID")
    access_token = os.environ.get("WHATSAPP_ACCESS_TOKEN")
    print(coupon_data.expiration_date)
    # coupon_params = [
    #     {
    #         "type": "text",
    #         "text": f"{coupon_data['coupon_code']}",
    #     },
    #     {
    #         "type": "text",
    #         "text": f"https://{os.environ.get('DOMAIN','shelterkart.com')}/listing/{coupon_data['fk_listing']}",  # noqa
    #     },
    #     {
    #         "type": "date_time",
    #         "date_time": {"fallback_value": coupon_data["expiration_date"]},
    #     },
    # ]

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    body = {
        "messaging_product": "whatsapp",
        "to": f"{reciepient_phone_number[1:]}",
        "type": "template",
        "template": {
            "name": f"{message_template_name}",
            "language": {"code": "en_US"},
            # "components": [{"type": "body", "parameters": coupon_params}], #TODO: Change when message template gets approved # noqa
        },
    }

    print(body)
    print(headers)

    try:
        response = requests.post(
            f"{WHATSAPP_API_URL}{phone_id}/messages",
            headers=headers,
            data=json.dumps(body),
        )
        print(response.status_code, response.json())
        return (response.status_code, response.json())
    except Exception as e:
        print(e)
        return (500, {"error": "Internal Server Error"})


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    if isinstance(exc, Throttled):  # check that a Throttled exception is raised
        custom_response_data = {  # prepare custom response data
            "message": "request throttled",
            "time": exc.wait,
        }
        print(exc, "===============util 62=====================\n", Throttled)
        response.data = (
            custom_response_data  # set the custom response data on response object
        )

    return response
