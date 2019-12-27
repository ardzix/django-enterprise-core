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
from datetime import date
from dateutil.relativedelta import relativedelta
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.postgres.fields import ArrayField
from django.conf import settings

from enterprise.libs import base36
from enterprise.libs.moment import to_timestamp
from enterprise.libs.decimal_lib import dec_to_str
from enterprise.libs.pay_constants import (WITHDRAW_STATUSES, INVOICE_STATUSES,
                                      PAYMENT_STATUSES, TOPUP_STATUSES)
from enterprise.structures.common.models import BaseModelGeneric

from .midtrans import Midtrans
from .manual import Manual

User = settings.AUTH_USER_MODEL


class Wallet(BaseModelGeneric):
    amount = models.DecimalField(max_digits=19, decimal_places=2)
    description = models.CharField(max_length=200, blank=True, null=True)
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, blank=True, null=True)
    object_id = models.PositiveIntegerField(blank=True, null=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return "%s:%s" % (self.created_by, self.amount)

    def get_formatted_amount(self):
        return 'Rp.{:,.0f},-'.format(self.amount)

    def get_absolute_formatted_amount(self):
        return 'Rp.{:,.0f},-'.format(abs(self.amount))

    class Meta:
        verbose_name = _("Wallet")
        verbose_name_plural = _("Wallet")


class Invoice(BaseModelGeneric):
    number = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=19, decimal_places=2)
    status = models.CharField(
        max_length=20, choices=INVOICE_STATUSES, default='pending')

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

    def get_formatted_amount(self):
        return 'Rp.{:,.0f},-'.format(self.amount)

    class Meta:
        verbose_name = _("Invoice")
        verbose_name_plural = _("Invoices")


class InvoiceItem(BaseModelGeneric):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=19, decimal_places=2)
    qty = models.PositiveIntegerField(default=1)
    name = models.CharField(max_length=50, blank=True, null=True)
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, blank=True, null=True)
    object_id = models.PositiveIntegerField(blank=True, null=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return "%s:%s" % (self.name, self.get_total_amount())

    def get_total_amount(self):
        return decimal.Decimal(self.qty) * self.amount

    def get_formatted_total_amount(self):
        return 'Rp.{:,.0f},-'.format(self.get_total_amount())

    def get_formatted_amount(self):
        return 'Rp.{:,.0f},-'.format(self.amount)

    class Meta:
        verbose_name = _("Invoice Item")
        verbose_name_plural = _("Invoice Items")


class TopUp(BaseModelGeneric):
    amount = models.DecimalField(max_digits=19, decimal_places=2)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    midtrans = models.ForeignKey(
        Midtrans,
        on_delete=models.CASCADE,
        blank=True, null=True
    )
    manual = models.ForeignKey(
        Manual,
        on_delete=models.CASCADE,
        blank=True, null=True
    )
    expired_at = models.DateTimeField(blank=True, null=True)
    status = models.CharField(
        max_length=20, choices=TOPUP_STATUSES, default='pending')

    def __str__(self):
        return "%s - %s" % (self.created_by, self.amount, )

    def approve(self, *args, **kwargs):
        self.status = 'approve'
        self.save(*args, **kwargs)

    def deny(self, *args, **kwargs):
        self.status = 'deny'
        self.save(*args, **kwargs)

    def get_formatted_amount(self):
        return 'Rp.{:,.0f},-'.format(self.amount)

    class Meta:
        verbose_name = _("Top Up")
        verbose_name_plural = _("Top Up")


# Bank
class Bank(BaseModelGeneric):
    display_name = models.CharField(max_length=100)
    short_name = models.SlugField(max_length=100)
    code = models.SlugField(max_length=100)

    def __str__(self):
        return self.display_name

    class Meta:
        verbose_name = _("Bank")
        verbose_name_plural = _("Banks")


class BankAccount(BaseModelGeneric):
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)
    number = models.CharField(max_length=20)
    name = models.CharField(max_length=120)
    notes = models.TextField(blank=True, null=True)  # branch name, etc.d

    def __str__(self):
        return '%s (%s:%s)' % (self.name, self.bank.__str__(), self.number)

    class Meta:
        verbose_name = _("Bank Account")
        verbose_name_plural = _("Bank Accounts")


class Withdraw(BaseModelGeneric):
    # use : created_by, approved_by; created_by = requester, approved_by = managed_by
    balance = models.DecimalField(max_digits=19, decimal_places=2)
    amount = models.DecimalField(max_digits=19, decimal_places=2)
    status = models.CharField(
        max_length=20, choices=WITHDRAW_STATUSES, default="pending")
    bank_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE)
    expired_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return "%s:%s" % (self.get_formatted_amount(), self.created_by)

    def get_formatted_amount(self):
        return 'Rp.{:,.0f},-'.format(self.amount)

    def get_formatted_balance(self):
        return 'Rp.{:,.0f},-'.format(self.balance)

    class Meta:
        verbose_name = _("Withdraw")
        verbose_name_plural = _("Withdraws")


@receiver(post_save, sender=TopUp)
def do_topup(sender, instance, created, **kwargs):
    from enterprise.libs.payment.wallet import topup_wallet, transfer_wallet

    if instance.status == "approve":
        topup_wallet(
            topup=instance,
            description="TopUp wallet <invoice: %s>" % instance.invoice.number
        )

        for item in instance.invoice.get_items():
            print(item)
            print("transfering balance")
            if item.content_object:
                receiver = item.content_object.owned_by
                transfer_wallet(
                    instance.owned_by,
                    receiver,
                    int(item.amount),
                    obj=item,
                    description='%s: %s' % (
                        item.content_type.__str__(),
                        item.name
                    )
                )
        instance.status = 'success'
        instance.save()


def get_default_data():
    return [1]
