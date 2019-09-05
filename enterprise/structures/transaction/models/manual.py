'''
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# File: manual.py
# Project: <<projectname>>
# File Created: Friday, 24th May 2019 9:16:46 pm
# 
# Author: Arif Dzikrullah
#         ardzix@hotmail.com>
#         http://ardz.xyz>
# 
# Last Modified: Friday, 24th May 2019 9:16:47 pm
# Modified By: arifdzikrullah (ardzix@hotmail.com>)
# 
# Crafted by Pro
# Copyright - <<year>> Ardz & Co, -
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''


from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import JSONField

from enterprise.libs.payment.midtrans import PAYMENT_STATUSES
from enterprise.libs import storage
from enterprise.structures.common.models import BaseModelGeneric


class Manual(BaseModelGeneric):
    transaction_status = models.CharField(
        choices=PAYMENT_STATUSES, max_length=40, default='pending')
    amount = models.DecimalField(default=0, decimal_places=2, max_digits=12)
    attachement = models.FileField(
        storage=storage.FILE_STORAGE,
        max_length=300,
        blank=True,
        null=True
    )

    def __str__(self):
        return "%s : %s <%s>" % (
            self.created_by,
            self.amount,
            self.transaction_status
        )

    class Meta:
        verbose_name = _("Manual")
        verbose_name_plural = _("Manuals")