from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models import JSONField
from enterprise.libs.payment.midtrans import PAYMENT_STATUSES, PAYMENT_TYPE_CHOICES
from enterprise.structures.common.models import BaseModelGeneric

class Dana(BaseModelGeneric):
    transaction_status = models.CharField(choices=PAYMENT_STATUSES, max_length=40)
    transaction_id = models.CharField(max_length=40, blank=True, null=True)
    amount = models.DecimalField(default=0, decimal_places=2, max_digits=12)
    payload = JSONField(blank=True, null=True)
    responses = JSONField(blank=True, null=True)
    checkout_url = models.TextField()

    def __str__(self):
        return "%s : %s <%s>" % (
            self.created_by,
            self.amount,
            self.transaction_status
        )

    class Meta:
        verbose_name = _("Dana")
        verbose_name_plural = _("Dana")
