from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models import JSONField
from enterprise.libs.payment.midtrans import PAYMENT_STATUSES, PAYMENT_TYPE_CHOICES
from enterprise.libs.model import BaseModelGeneric

class Shopeepay(BaseModelGeneric):
    transaction_status = models.CharField(choices=PAYMENT_STATUSES, max_length=40)
    transaction_id = models.CharField(max_length=40, blank=True, null=True)
    amount = models.DecimalField(default=0, decimal_places=2, max_digits=12)
    payload = JSONField(blank=True, null=True)
    responses = JSONField(blank=True, null=True)
    
    shoppepay_id = models.CharField(max_length=60, blank=True, null=True)
    business_id = models.CharField(max_length=40, blank=True, null=True)
    currency = models.CharField(max_length=10, blank=True, null=True)
    capture_amount = models.DecimalField(default=0, decimal_places=2, max_digits=12)
    checkout_method = models.CharField(max_length=40, blank=True, null=True)
    channel_code = models.CharField(max_length=40, blank=True, null=True)
    channel_properties = JSONField(blank=True, null=True)
    actions = JSONField(blank=True, null=True)
    is_redirect_required  = models.BooleanField(blank=True, null=True)
    callback_url = models.TextField(blank=True, null=True)
    created = models.CharField(max_length=40, blank=True, null=True)
    updated = models.CharField(max_length=40, blank=True, null=True)
    voided_at = models.CharField(max_length=40, blank=True, null=True)
    capture_now = models.BooleanField(blank=True, null=True)
    customer_id = models.CharField(max_length=40, blank=True, null=True)
    payment_method_id = models.CharField(max_length=40, blank=True, null=True)
    failure_code = models.CharField(max_length=40, blank=True, null=True)
    basket = JSONField(blank=True, null=True)
    metadata = JSONField(blank=True, null=True)
    
    checkout_url = models.TextField(blank=True, null=True)

    def __str__(self):
        return "%s : %s <%s>" % (
            self.created_by,
            self.amount,
            self.transaction_status
        )

    class Meta:
        verbose_name = _("Shopeepay")
        verbose_name_plural = _("Shopeepay")
