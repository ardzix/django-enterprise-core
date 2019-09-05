'''
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# File: midtrans.py
# Project: core.wecare.id
# File Created: Monday, 7th January 2019 10:15:09 pm
# 
# Author: Arif Dzikrullah
#         ardzix@hotmail.com>
#         https://github.com/ardzix/>
# 
# Last Modified: Monday, 7th January 2019 10:15:09 pm
# Modified By: arifdzikrullah (ardzix@hotmail.com>)
# 
# Handcrafted and Made with Love
# Copyright - 2018 Wecare.Id, wecare.id
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''


import requests
import base64
import json
import ssl
import datetime

from django.urls.base import NoReverseMatch
from django.shortcuts import reverse
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder

PAYMENT_TYPE_CHOICES = (
    ('gopay', _('GoPay')),
    ('telkomsel_cash', _('Telkomsel Cash')),
    ('indosat_dompetku', _('Indosat Dompetku')),
    ('mandiri_ecash', _('LINE Pay e-cash|mandiri e-cash')),
    ('bca_klikpay', _('BCA Klickpay')),
    ('bca_klikbca', _('Klik BCA')),
    ('mandiri_clickpay', _('Mandiri Klikpay')),
    ('bri_epay', _('Epay BRI')),
    ('cimb_clicks', _('CIMB Clicks')),
    ('bank_transfer', _('Bank Transfer')),
    ('credit_card', _('Credit Card')),
)

PAYMENT_STATUSES = (
    ('authorize', _('Transaction authorizes the credit card.')),
    ('capture', _('Transaction captures the credit card balance. Will be settled as batch.')),
    ('settlement', _('Transaction is settled.')),
    ('deny', _('Payment provider rejects the credentials used for payment.')),
    ('pending', _('Transaction is made available in Midtrans to be paid.')),
    ('cancel', _('Transaction is cancelled.')),
    ('refund', _('Transaction is marked to be refunded.')),
    ('partial_refund', _('Transaction is marked to be partially refunded.')),
    ('chargeback', _('Transaction is marked to be charged back.')),
    ('partial_chargeback', _('Transaction is marked to be partially charged back.')),
    ('expire', _('Transaction no longer available to be paid or processed')),
    ('failure', _('Unexpected error during transaction processing')),

    ('preparing', _('Preparing data for transaction to midtrans'))
)


class _BaseMidtransPay(object):
    '''
    Abstract class for payment with midtrans
    '''
    payload = {}
    invoice = None

    def __init__(self, payment_type, invoice):
        self.invoice = invoice
        self.payload['payment_type'] = payment_type

        if invoice:
            user = invoice.created_by
            self.add_customer_details({
                'first_name': user.full_name,
                'email': user.email,
                'phone': user.phone_number,
            })
            try:
                self.add_callbacks(
                    {
                        'finish': '%s?inv=%s' % (
                            reverse('donation:success'), 
                            invoice.number
                        ),
                        'pending': '%s?inv=%s' % (
                            reverse('payment:status'), 
                            invoice.number
                        ),
                    }
                )
            except NoReverseMatch as e:
                print(e)

            items = []
            for item in invoice.get_items():
                items.append({
                    "id": item.id62,
                    "price": int(item.amount),
                    "quantity": item.qty,
                    "name": item.item_name,
                })
            self.add_item_details(items)

    def add_payload(self, *args, **kwargs):
        self.payload = {**self.payload, **kwargs}

    def add_customer_details(self, data):
        self.add_payload(customer_details = data)
    
    def add_callbacks(self, data):
        self.add_payload(callbacks = data)
    
    def add_item_details(self, data):
        self.add_payload(item_details = data)

    def set_transaction_details(self, order_id, gross_amount):
        if getattr(settings, 'PRODUCTION', False) is False:
            order_id = '%s-%s-%s' %(
                order_id.split('-')[0],
                datetime.datetime.timestamp(datetime.datetime.now()),
                order_id.split('-')[1]
            )

        transaction_details = {
            'order_id' : order_id,
            'gross_amount' : gross_amount
        }
        self.add_payload(transaction_details=transaction_details)

    def get_payload(self):
        return self.payload

    def request(self, url):
        basic_auth = '%s:' % getattr(settings, 'API_SERVER_KEY')
        encoded_basic_auth = base64.b64encode(basic_auth.encode()).decode('utf-8')
        headers = {
            'Content-Type' : 'application/json',
            'Accept' : 'application/json',
            'Authorization' : 'Basic %s' % encoded_basic_auth
        }
        print(self.payload)
        r = requests.post(url, data=json.dumps(self.payload, cls=DjangoJSONEncoder), headers=headers)
        r_dict = r.json()

        return r_dict

    def charge(self, user, amount):
        from enterprise.structures.transaction.models.midtrans import Midtrans

        if not self.invoice:
            raise Exception('Invoice is null')

        midtrans = Midtrans(
            payment_type = self.payload['payment_type'],
            transaction_status = 'preparing',
            amount = amount,
            payload = self.payload
        )
        midtrans.created_by = user
        midtrans.save()

        self.set_transaction_details(order_id=self.invoice.number+'-'+midtrans.id62, gross_amount=int(amount))

        result = self.request(self.get_charge_url())
        if 'transaction_id' in result:
            midtrans.transaction_id = result['transaction_id']
        if 'transaction_status' in result:
            midtrans.transaction_status = result['transaction_status']
        midtrans.responses = result
        midtrans.save()
        return result

    def get_charge_url(self):
        return '%s/v2/charge' % getattr(settings, 'API_URL',
                                        'https://api.sandbox.midtrans.com')


class Gopay(_BaseMidtransPay):
    def __init__(self, invoice, *args, **kwargs):
        callback_url = kwargs.get('callback_url')
        super(Gopay, self).__init__('gopay', invoice=invoice)
        self.add_payload(
            gopay = {
                'enable_callback' : True if callback_url else False,
                'callback_url' : callback_url
            }
        )


class BankTransfer(_BaseMidtransPay):
    def __init__(self, invoice, *args, **kwargs):
        super(BankTransfer, self).__init__('bank_transfer', invoice=invoice)
        self.add_payload(
            bank_transfer = {
                'bank' : kwargs.get('bank'),
            }
        )


class MandiriEChannel(_BaseMidtransPay):
    def __init__(self, invoice, *args, **kwargs):
        super(MandiriEChannel, self).__init__('echannel', invoice=invoice)
        self.add_payload(
            echannel = {
                'bill_info1' : 'Payment for invoice %s' % invoice.number,
                'bill_info2' : 'debt',
            }
        )


class CreditCard(_BaseMidtransPay):
    def __init__(self, invoice, *args, **kwargs):
        super(CreditCard, self).__init__('credit_card', invoice=invoice)
        self.add_payload(
            credit_card = {
                'card': kwargs.get('card'),
                'dynamic_descriptor': {
                    'merchant_name': 'Wecare.Id',
                    'city_name': 'Jakarta',
                    'country_code': 'ID'
                },
                'authentication': True,
                'callback_type': 'js_event'
            }
  
        )

class Snap(_BaseMidtransPay):
    def __init__(self, invoice, *args, **kwargs):
        super(Snap, self).__init__('snap', invoice=invoice)
        payment_channel = kwargs.get('payment_channel')
        if not payment_channel:
            payment_channel = PAYMENT_TYPE_CHOICES
        self.add_payload(credit_card = {'secure':True})
        self.add_payload(enabled_payments = list(k for k,v in payment_channel))

    def get_charge_url(self):
        return '%s/snap/v1/transactions' % getattr(settings, 'APP_URL',
                                        'https://app.sandbox.midtrans.com')