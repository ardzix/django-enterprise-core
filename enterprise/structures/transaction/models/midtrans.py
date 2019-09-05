'''
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# File: midtrans.py
# Project: core.wecare.id
# File Created: Monday, 7th January 2019 11:03:02 pm
#
# Author: Arif Dzikrullah
#         ardzix@hotmail.com>
#         https://github.com/ardzix/>
#
# Last Modified: Monday, 7th January 2019 11:03:02 pm
# Modified By: arifdzikrullah (ardzix@hotmail.com>)
#
# Handcrafted and Made with Love
# Copyright - 2018 Wecare.Id, wecare.id
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''


from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import JSONField
from enterprise.libs.payment.midtrans import PAYMENT_STATUSES, PAYMENT_TYPE_CHOICES
from enterprise.structures.common.models import BaseModelGeneric


class Midtrans(BaseModelGeneric):
    payment_type = models.CharField(
        choices=PAYMENT_TYPE_CHOICES, max_length=40)
    transaction_status = models.CharField(
        choices=PAYMENT_STATUSES, max_length=40)
    transaction_id = models.CharField(max_length=40, blank=True, null=True)
    amount = models.DecimalField(default=0, decimal_places=2, max_digits=12)
    payload = JSONField(blank=True, null=True)
    responses = JSONField(blank=True, null=True)

    def __str__(self):
        return "%s : %s <%s>" % (
            self.created_by,
            self.amount,
            self.transaction_status
        )

    class Meta:
        verbose_name = _("Midtrans")
        verbose_name_plural = _("Midtranses")
