import requests
import json

from django.conf import settings

WAVECELL_API_KEY = getattr(settings, 'WAVECELL_API_KEY', '')
WAVECELL_SUB_ACC = getattr(settings, 'WAVECELL_SUB_ACC', '')
DEFAULT_TEMPLATE = "JAGA KERAHASIAAN ANDA, KODE TIDAK UNTUK DIBAGIKAN. Kode RAHASIA anda adalah {code}"


class Wavecell(object):
    def __init__(self, *args, **kwargs):
        # validate key
        if not WAVECELL_API_KEY or not WAVECELL_SUB_ACC:
            raise Exception('%s is required. Please put at settings.' % (
                "WAVECELL_SUB_ACC" if not WAVECELL_SUB_ACC else "WAVECELL_API_KEY"))

        # get information
        self.template = kwargs.get('template', DEFAULT_TEMPLATE)
        self.brand = kwargs.get('brand', 'Django Enterprise')
        self.headers = {
            "Authorization": "Bearer %s" % WAVECELL_API_KEY
        }

        self.base_url = "https://api.wavecell.com/verify/v2/"

    def request_otp(self, phone_number, otp_length=6):
        url = self.base_url + WAVECELL_SUB_ACC
        headers = self.headers
        template = self.template
        brand = self.brand
        session_id = None
        errors = None

        body = {
            "destination": "%s" % phone_number,
            "country": "ID",
            "brand": brand,
            "codeLength": otp_length,
            "template": template,
            "codeType": "NUMERIC",
            "channel": "sms",
            "sms": {
                "source": brand,
                "encoding": "AUTO"
            }
        }

        response = requests.post(url, headers=headers, json=body)

        if response.status_code == 200:
            res_data = json.loads(response.text)
            session_id = res_data.get('sessionId')
        else:
            errors = dict(json.loads(response.text))

        return session_id, errors

    def verify_otp(self, session_id, code):
        headers = self.headers
        url = "{}{}/{}?code={}".format(self.base_url,
                                       WAVECELL_SUB_ACC, session_id, code)

        response = requests.get(url, headers=headers)

        status_code = response.status_code
        errors = None
        is_valid = False

        if status_code == 404:
            errors = "Your request OTP is expired. Please request again"
        elif status_code != 200 or (status_code == 200 and response.json().get('status') != 'VERIFIED'):
            errors = "Invalid session_id or OTP code. Please check again."
            status_code = 400
        else:
            is_valid = True

        return is_valid, errors
