import requests
import hashlib
import json
from django.conf import settings
from uuid import uuid4
from datetime import datetime
from django.core.serializers.json import DjangoJSONEncoder
from rest_framework import mixins, viewsets, status
from rest_framework.response import Response


SIGNATURE_KEY = getattr(settings, 'ESPAY_SIGNATURE_KEY', '')
API_KEY = getattr(settings, 'ESPAY_API_KEY', '')


class _BaseEspay(object):
    '''
    Abstract class for payment with espay
    '''
    payload = {}
    invoice = None
    request_status_code = None

    def __init__(self, invoice):
        self.invoice = invoice

    def get_order_id(self, espay_id62):
        order_id = self.invoice.number+'-'+espay_id62
        if not getattr(settings, 'PRODUCTION', False):
            order_id = '%s-%s-%s' % (
                order_id.split('-')[0],
                datetime.timestamp(datetime.now()),
                order_id.split('-')[1]
            )
        return order_id

    def add_payload(self, *args, **kwargs):
        self.payload = {**self.payload, **kwargs}

    def request(self, url):
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        r = requests.post(url, data=self.payload, headers=headers)
        r_dict = r.json()
        self.request_status_code = r_dict.get('status_code')

        return r_dict

    def get_send_invoice_url(self):
        return '%sdigitalpay/pushtopay' % getattr(settings, 'ESPAY_API_URL',
                                                   'https://sandbox-api.espay.id/rest/')

    def get_signature(self, bare_signature):
        upper_signature = bare_signature.upper()
        signature = hashlib.sha256(upper_signature.encode()).hexdigest()
        return signature


class EspayPG(_BaseEspay):

    def send_invoice(self, bank_code):
        from enterprise.structures.transaction.models.espay import Espay

        invoice = self.invoice
        invoice.published_at = datetime.now()
        invoice.save()
        user = invoice.owned_by

        if not self.invoice:
            raise Exception('Invoice is null')

        amount = invoice.amount
        espay = Espay(
            payment_type=bank_code,
            transaction_status='preparing',
            amount=amount,
            payload=self.payload
        )
        espay.created_by = user
        espay.save()

        rq_uuid = uuid4()
        rq_datetime = datetime.now()
        order_id = self.get_order_id(espay.id62)
        ccy = getattr(settings, 'ESPAY_CCY', 'IDR')
        comm_code = getattr(settings, 'ESPAY_COMMERCE_CODE', 'SGWSOCIALITTA')
        remark1 = user.phone_number
        remark2 = user.full_name
        remark3 = user.email
        update = 'N'
        va_expired = getattr(settings, 'ESPAY_VA_EXPIRED_MINUTE', '120')
        bare_signature = '##%s##%s##%s##%s##%s##%s##%s##SENDINVOICE##' % (
            SIGNATURE_KEY,
            rq_uuid,
            rq_datetime,
            order_id,
            amount,
            ccy,
            comm_code,
        )
        signature = self.get_signature(bare_signature)

        payload = {
            'rq_uuid': rq_uuid,
            'rq_datetime': rq_datetime,
            'order_id': order_id,
            'amount': amount,
            'ccy': ccy,
            'comm_code': comm_code,
            'remark1': remark1,
            'remark2': remark2,
            'remark3': remark3,
            'bank_code': bank_code,
            'update': update,
            'va_expired': va_expired,
            'signature': signature
        }
        self.add_payload(payload)

        result = self.request(self.get_send_invoice_url())
        espay.responses = result
        espay.save()
        return result


class BankView(viewsets.GenericViewSet, mixins.ListModelMixin):

    def get_serializer(self, *args, **kwargs):
        return None

    def list(self, request):
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        url = '%smerchant/merchantinfo' % getattr(settings, 'ESPAY_API_URL',
                                                   'https://sandbox-api.espay.id/rest/')
        r = requests.post(url, data={'key': API_KEY}, headers=headers)
        resp = r.json()

        if not 'error_code' in resp:
            return Response(
                {'error_message': r.text},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if resp.get('error_code') != '0000':
            return Response(
                {'error_message': resp.get('error_message')},
                status=status.HTTP_400_BAD_REQUEST
            )
        data = resp.get('data')
        return Response(
            resp.get('data'),
            status=status.HTTP_200_OK
        )
