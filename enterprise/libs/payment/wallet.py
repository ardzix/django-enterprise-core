'''
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# File: wallet.py
# Project: <<projectname>>
# File Created: Friday, 24th May 2019 9:10:35 pm
# 
# Author: Arif Dzikrullah
#         ardzix@hotmail.com>
#         http://ardz.xyz>
# 
# Last Modified: Friday, 24th May 2019 9:10:35 pm
# Modified By: arifdzikrullah (ardzix@hotmail.com>)
# 
# Crafted by Pro
# Copyright - <<year>> Ardz & Co, -
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''

import datetime
from decimal import Decimal
from django.db.models import Sum
from ...structures.transaction.models import Wallet


def get_balance(user):
    balance = Wallet.objects.filter(
        owned_by=user, deleted_at__isnull=True,
        ).aggregate(Sum('amount'))['amount__sum']
    return balance if balance is not None else Decimal(0)

def transfer_wallet(from_user, to_user, total, obj=None, description="Transfer balance"):

    if total <= 0:
        raise Exception("Total transfer must be greater than zero")

    if from_user == to_user:
        raise Exception("Cannot transfer to same user (user:%s, obj:%s)" %
                (
                    str(from_user),
                    str(obj) if obj else '-'
                )
            )

    current_balance = get_balance(from_user)
    if current_balance < total:
        raise Exception("Insufficient balance %d:%d" % (current_balance, total))

    # deduct first
    wallet = Wallet()
    wallet.created_by = from_user
    wallet.amount = total * -1 if total > 0 else total
    wallet.description = description
    if obj:
        wallet.content_type = obj.get_content_type()
        wallet.object_id = obj.id
    wallet.save()
    print("Deduction success")

    # add credit
    wallet = Wallet()
    wallet.created_by = to_user
    wallet.amount = total * -1 if total < 0 else total
    wallet.description = description
    if obj:
        wallet.content_type = obj.get_content_type()
        wallet.object_id = obj.id
    wallet.save()
    print("Addition Success")
    print("Current balance now %s" % str(current_balance - total))
    return True

def topup_wallet(topup, description="Topup balance"):

    wallet = Wallet.objects.create(
        created_by = topup.owned_by,
        content_type = topup.get_content_type(),
        object_id = topup.id,
        amount = topup.amount
    )
    wallet.description = description
    wallet.save()
    print("Topup Success for %s" % wallet.description)
    return True

def deduct_wallet(user, amount, obj=None, description="Deduction"):
    current_balance = get_balance(user)
    if current_balance < amount:
        raise Exception("Insufficient balance %d:%d" % (current_balance, amount))

    # deduct first
    wallet = Wallet()
    wallet.created_by = user
    wallet.amount = amount * -1 if amount > 0 else amount
    wallet.description = description
    if obj:
        wallet.content_type = obj.get_content_type()
        wallet.object_id = obj.id
    wallet.save()
    print("Deduction success (%s)" % amount)
    print(wallet)
    return True


class WalletChannelManager(object):
    invoice = None

    def __init__(self, *args, **kwargs):
        self.invoice = kwargs.get('invoice')

    def charge(self, user, amount):
        if not self.invoice:
            raise Exception("Invoice not provided")

        if self.invoice.status == 'settlement':
            raise Exception("Invoice already paid")

        items = []
        for item in self.invoice.get_items():
            items.append({
                'name' : item.name,
                'qty' : item.qty,
                'amount' : item.amount,
            })

            receiver = item.content_object.owned_by

            transfer_wallet(
                user, 
                receiver, 
                int(item.amount * item.qty),
                obj = item,
                description = '%s: %s%s' % (
                    item.content_type.__str__(),
                    item.name,
                    ' x%d' % item.qty if item.qty >1 else ''
                )
            )

        self.invoice.status = 'settlement'
        self.invoice.updated_by = user
        self.invoice.save()

        return {
            'message': 'Transfer success',
            'items':items
        }