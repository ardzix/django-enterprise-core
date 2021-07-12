'''
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# File: otp.py
# Project: django-panel-core
# File Created: Tuesday, 25th February 2020 12:57:24 am
# 
# Author: Arif Dzikrullah
#         ardzix@hotmail.com>
#         https://github.com/ardzix/>
# 
# Last Modified: Tuesday, 25th February 2020 12:57:24 am
# Modified By: Arif Dzikrullah (ardzix@hotmail.com>)
# 
# Hand-crafted & Made with Love
# Copyright - 2018 Ardz Co, https://github.com/ardzix/django-panel-core
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''
import random
import json

from django.conf import settings
from datetime import datetime, timedelta

from enterprise.libs.sms import Wavecell, Nexmo

RANGE_OTP_ATTEMPT = getattr(settings, "RANGE_OTP_ATTEMPT", 1)  # value in hour
MAX_OTP_ATTEMPT = getattr(settings, "MAX_OTP_ATTEMPT", 4)
SMS_GATEWAY_PROVIDER = getattr(settings, "SMS_GATEWAY_PROVIDER", "wavecell")
AVAILABLE_SMS_GATEWAY = ['nexmo', 'wavecell']


def generate_otp_code(length):
    """Generate OTP code with custom length

    Arguments:
        length {integer} -- Length of code [Max 6]
    """

    otp = ""
    for i in range(length):
        otp += str(random.randint(1, 9))

    return otp


class OTPManager(object):
    def __init__(self, *args, **kwargs):
        phone_number = kwargs.get('phone_number')
        user = kwargs.get('user')

        if not phone_number:
            raise ValueError('kwargs phone_number is required')

        self.template = kwargs.get('template')
        self.provider = self.get_sms_gatewey(SMS_GATEWAY_PROVIDER)
        self.phone_number = phone_number
        self.user = user
        self.brand = kwargs.get('brand')
        self.otp_length = kwargs.get('otp_length')

        # instance class provider
        if self.provider == 'wavecell':
            self.provider_instance = Wavecell(
                brand=self.brand, template=self.template)
        elif self.provider == 'nexmo':
            self.provider_instance = Nexmo(brand=self.brand)

    def get_sms_gatewey(self, sg_type):
        if sg_type not in AVAILABLE_SMS_GATEWAY:
            raise ValueError("%s not available." % sg_type)

        return sg_type

    def is_limit_exceeded(self):
        '''
        This method should be return true if phone number has reached limit attempt
        Limit attempt can be setting at settings.py
        '''
        from enterprise.structures.authentication.models import OTPAttempt

        phone_number = self.phone_number
        periode = datetime.now() - timedelta(hours=RANGE_OTP_ATTEMPT)
        otp_attempt = OTPAttempt.objects.filter(
            phone_number=phone_number,
            attempt_at__gte=periode
        ).count()

        if otp_attempt == MAX_OTP_ATTEMPT:
            return True
        return False

    def request_otp(self, *args, **kwargs):
        from enterprise.structures.authentication.models import OTPAttempt

        request_id = None
        errors = None
        phone_number = self.phone_number
        user = self.user
        otp_length = self.otp_length
        provider_instance = self.provider_instance

        is_limit_exceeded = self.is_limit_exceeded()

        if is_limit_exceeded:
            errors = f"Sending OTP to {phone_number} has exceeded allowed limit of max attempt."

            return request_id, errors

        request_id, errors = provider_instance.request_otp(
            phone_number, otp_length=otp_length)

        # insert to OTP attempt
        OTPAttempt.objects.create(
            phone_number=phone_number,
            user=user
        )

        return request_id, errors

    def validate_otp(self, session_id, code):
        """ validate OTP with session_id and code

        Args:
            session_id (string): got from request OTP
            code (integer): got from SMS

        Returns:
            - is_valid -- boolean: return True if valid
            - errors -- string: error when validate
        """

        provider_instance = self.provider_instance
        return provider_instance.verify_otp(session_id, code)
