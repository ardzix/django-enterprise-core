'''
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# File: xendit.py
# Project: core.wecare.id
# File Created: Saturday, 27th April 2019 1:23:38 pm
# 
# Author: Arif Dzikrullah
#         ardzix@hotmail.com>
#         https://github.com/ardzix/>
# 
# Last Modified: Saturday, 27th April 2019 1:23:38 pm
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

from django.utils.translation import gettext_lazy as _
from django.conf import settings


class Xendit(object):

    disbursement = None
    bank_account = None
    def __init__(self, disbursement, bank_account):
        self.disbursement = disbursement
        self.bank_account = bank_account

    def disburse(self):
        headers = {
            'X-IDEMPOTENCY-KEY' : self.disbursement.id62
        }
        data = {
            'external_id' : self.disbursement.nonce,
            'bank_code' : self.bank_account.bank.display_name,
            'account_holder_name' : self.bank_account.name,
            'account_number' : self.bank_account.number,
            'description' : self.disbursement.description,
            'amount' : self.disbursement.amount
        }
        r = requests.post(
            'https://api.xendit.co/disbursements', 
            headers=headers, 
            data=data, 
            auth=(getattr(settings, 'XENDIT_SECRET_KEY'), '')
        )
        r_dict = r.json()

        return r_dict
