import nexmo

from django.conf import settings

NEXMO_API_KEY = getattr(settings, 'NEXMO_API_KEY', '')
NEXMO_API_SECRET = getattr(settings, 'NEXMO_API_SECRET', '')
BRAND = getattr(settings, 'BRAND', 'Django Enterprise')


class Nexmo(object):
    def __init__(self, *args, **kwargs):
        if not NEXMO_API_KEY or not NEXMO_API_SECRET:
            raise Exception('%s is required. Please put at settings.' % (
                "NEXMO_API_SECRET" if not NEXMO_API_SECRET else "NEXMO_API_KEY"))

        client = nexmo.Client(key=NEXMO_API_KEY, secret=NEXMO_API_SECRET)

        self.client = client
        self.brand = kwargs.get('brand', BRAND)

    def request_otp(self, phone_number, otp_length=6):
        brand = self.brand
        client = self.client

        request_id = None
        errors = None

        response = client.start_verification(number=phone_number, brand=brand)
        if not response['status'] == '0' and not response['status'] == '10':
            errors = response['error_text']

        request_id = response.get('request_id')

        return request_id, errors

    def verify_otp(self, request_id, code):
        client = self.client
        response = client.check_verification(request_id, code=code)

        is_valid = True
        errors = None

        if not response['status'] == '0':
            is_valid = False
            errors = response['error_text']

        return is_valid, errors

    def send_sms(self, phone_number, text):
        pass