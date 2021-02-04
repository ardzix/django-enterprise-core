from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models import JSONField
from enterprise.libs.payment.midtrans import PAYMENT_STATUSES, PAYMENT_TYPE_CHOICES
from enterprise.structures.common.models import BaseModelGeneric

class Jenius(BaseModelGeneric):
    transaction_status = models.CharField(choices=PAYMENT_STATUSES, max_length=40)
    transaction_id = models.CharField(max_length=40, blank=True, null=True)
    amount = models.DecimalField(default=0, decimal_places=2, max_digits=12)
    payload = JSONField(blank=True, null=True)
    responses = JSONField(blank=True, null=True)
    cashtag = models.CharField(max_length=40)
    promo_code = models.CharField(max_length=40,blank=True,null=True)
    description = models.TextField(blank=True, null=True)
    original_transmission_datetime = models.CharField(max_length=40, blank=True, null=True)
    approval = models.CharField(max_length=40,blank=True,null=True)

    def __str__(self):
        return "%s : %s <%s>" % (
            self.created_by,
            self.amount,
            self.transaction_status
        )

    class Meta:
        verbose_name = _("Jenius")
        verbose_name_plural = _("Jenius")
