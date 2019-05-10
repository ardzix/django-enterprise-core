'''
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# File: __init__.py
# Project: core.ayopeduli.id
# File Created: Thursday, 1st November 2018 1:16:00 am
# 
# Author: Arif Dzikrullah
#         ardzix@hotmail.com>
#         https://github.com/ardzix/>
# 
# Last Modified: Thursday, 1st November 2018 1:16:05 am
# Modified By: arifdzikrullah (ardzix@hotmail.com>)
# 
# Peduli sesama, sejahtera bersama
# Copyright - 2018 Ayopeduli.Id, ayopeduli.id
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''


import decimal
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.postgres.fields import ArrayField

from panel.structures.authentication.models import User
from panel.structures.common.models import BaseModelGeneric

from panel.libs import base36
from panel.libs.decimal_lib import dec_to_str
from panel.libs.pay_constants import (CASHOUT_STATUSES, INVOICE_STATUSES, BANK_CHOICES,
                                    PAYMENT_STATUSES, SUBSCRIPTION_CHARGE_METHOD)


class Wallet(BaseModelGeneric):
    amount = models.DecimalField(max_digits=19, decimal_places=2)
    description = models.CharField(max_length=200, blank=True, null=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, blank=True, null=True)
    object_id = models.PositiveIntegerField(blank=True, null=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return "%s:%s" % (self.created_by.full_name, self.amount)

    def get_formatted_amount(self):
        return 'Rp.{:,.0f},-'.format(self.amount)

    class Meta:
        verbose_name = _("Wallet")
        verbose_name_plural = _("Wallet")


class Invoice(BaseModelGeneric):
    number = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=19, decimal_places=2)
    status = models.CharField(max_length=20, choices=INVOICE_STATUSES)

    def __str__(self):
        return str(self.number)

    def create_number(self, *args, **kwargs):
        if not self.number and self.pk:
            CONSTANT_START_NUMBER = 11470
            number = self.pk + CONSTANT_START_NUMBER
            self.number = '{}{}'.format("I", base36.encode(number))
            self.save()

    def get_items(self):
        return InvoiceItem.objects.filter(
            deleted_at__isnull=True,
            invoice=self
        ).all()

    def get_status(self):
        return dict(INVOICE_STATUSES)[self.status]

    def save(self, *args, **kwargs):
        su = super(Invoice, self).save(*args, **kwargs)
        self.create_number()
        return su

    class Meta:
        verbose_name = _("Invoice")
        verbose_name_plural = _("Invoices")


class InvoiceItem(BaseModelGeneric):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=19, decimal_places=2)
    qty = models.PositiveIntegerField(default=1)
    item_name = models.CharField(max_length=50, blank=True, null=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, blank=True, null=True)
    object_id = models.PositiveIntegerField(blank=True, null=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return "%s:%s" % (self.item_name, self.get_total_amount())

    def get_total_amount(self):
        return decimal.Decimal(self.qty) * self.amount

    def get_formatted_total_amount(self):
        return 'Rp.{:,.0f},-'.format(self.get_total_amount())

    class Meta:
        verbose_name = _("Invoice Item")
        verbose_name_plural = _("Invoice Items")


class TopUp(BaseModelGeneric):
    amount = models.DecimalField(max_digits=19, decimal_places=2)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUSES)

    def __str__(self):
        return "%s - %s" % (self.created_by.full_name, self.amount, )

    class Meta:
        verbose_name = _("Top Up")
        verbose_name_plural = _("Top Up")


class BankAccount(BaseModelGeneric):
    bank = models.CharField(max_length=20, choices=BANK_CHOICES)
    number = models.CharField(max_length=20)
    name = models.CharField(max_length=120)
    notes = models.TextField(blank=True, null=True) # branch name, etc.d

    def __str__(self):
        return self.name

    def get_bank(self):
        if self.bank not in dict(BANK_CHOICES):
            return None
        return dict(BANK_CHOICES)[self.bank]

    class Meta:
        verbose_name = _("Bank Account")
        verbose_name_plural = _("Bank Accounts")


class CashOutSession(BaseModelGeneric):
    number = models.CharField(max_length=20)
    begin_at = models.DateTimeField()
    end_at = models.DateTimeField()
    processed_at = models.DateTimeField(blank=True, null=True)
    processed_by = models.ForeignKey(User, related_name='cashoutbatch_processed_by', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.number

    def set_number(self):
        self.number = to_timestamp(timezone.now())

    class Meta:
        app_label = "cashout"


class CashOutRequest(BaseModelGeneric):
    # use : created_by, approved_by; created_by = requester, approved_by = managed_by
    session = models.ForeignKey(CashOutSession, on_delete=models.CASCADE)
    last_pk = models.BigIntegerField()
    total_balance = models.DecimalField(max_digits=19, decimal_places=2)
    total_requested = models.DecimalField(max_digits=19, decimal_places=2)
    status = models.CharField(max_length=20, choices=CASHOUT_STATUSES, default="pending")

    def __str__(self):
        return "%s:%s" % (self.session.number, self.created_by)

    @property
    def batch(self):
        return self.session.number

    def get_buttons(self):
        buttons = [  
            {
                "style":"margin:2px", 
                "class":"btn btn-sm btn-danger btn-cons btn-animated from-left pg pg-arrow_right", 
                "on_click" : "delete_data", 
                "icon":"fa-trash", 
                "text": "Delete"
            } 
        ]

        button_str = ""
        for b in buttons:
            button_str += '<button type="button" style="'+b['style']+'" class="'+b['class']+'" onclick="'+b['on_click']+'(\''+self.id62+'\')"><span><i class="fa '+b['icon']+'"></i>&nbsp;'+b['text']+'</span></button>'

        return button_str

    class Meta:
        app_label = "cashout"

# Subscription
def get_default_data():
    return [1]

class Subscription(BaseModelGeneric):
    token = models.CharField(max_length=128, blank=True, null=True)
    charge_date = ArrayField(
        models.PositiveIntegerField(),
        default = get_default_data
    )
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(blank=True, null=True)
    charge_method = models.PositiveIntegerField(choices=SUBSCRIPTION_CHARGE_METHOD, default=1)
    is_active = models.BooleanField(default=True)
    inactivity_reason = models.TextField(blank=True, null=True)
    amount = models.PositiveIntegerField()

    class Meta:
        verbose_name = _("Subscription")
        verbose_name_plural = _("Subscriptions")


class SubscriptionPayment(models.Model):
    charged_at = models.DateTimeField(auto_now_add=True)
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    topup = models.ForeignKey(TopUp, on_delete=models.CASCADE, blank=True, null=True)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUSES)

    class Meta:
        verbose_name = _("Subscription Payment")
        verbose_name_plural = _("Subscription Payments")


@receiver(post_save, sender=TopUp)
def do_topup(sender, instance, created, **kwargs):
    from panel.libs.wallet import topup_wallet, transfer_wallet

    if created :
        if instance.invoice.status == "settlement":
            topup_wallet(
                topup = instance,
                description = "TopUp wallet <invoice: %s>" % instance.invoice.number
            )

            for k, item in enumerate(instance.invoice.get_items()):
                print(item)
                print("transfering balance")
                if item.content_object:
                    receiver = item.content_object.owned_by
                    if item.content_type.model == 'donation':
                        receiver = item.content_object.destination_content_object.owned_by
                    transfer_wallet(
                        instance.owned_by, 
                        receiver, 
                        int(item.amount),
                        obj = item,
                        description = '%s: %s' % (
                            item.content_type.__str__(),
                            item.item_name
                        )
                    )
        else:
            instance.permanent_delete()