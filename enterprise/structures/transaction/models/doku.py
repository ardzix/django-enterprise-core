from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models import JSONField
from enterprise.libs.payment.midtrans import PAYMENT_STATUSES, PAYMENT_TYPE_CHOICES
from enterprise.structures.common.models import BaseModelGeneric

class Doku(BaseModelGeneric):
    transaction_status = models.CharField(choices=PAYMENT_STATUSES, max_length=40)
    transaction_id = models.CharField(max_length=40, blank=True, null=True)
    payload = JSONField(blank=True, null=True)
    responses = JSONField(blank=True, null=True)

    # for VA
    payment_date_time = models.CharField(max_length=14, blank=True, null=True)
    purchase_currency = models.CharField(max_length=3, blank=True, null=True)
    payment_channel = models.CharField(max_length=20, blank=True, null=True)
    amount = models.DecimalField(default=0, decimal_places=2, max_digits=12)
    payment_code = models.CharField(max_length=50, blank=True, null=True)
    words = models.TextField()
    result_msg = models.CharField(max_length=20, blank=True, null=True)
    trans_id_merchant = models.CharField(max_length=30, blank=True, null=True)
    bank = models.CharField(max_length=100, blank=True, null=True)
    status_type = models.CharField(max_length=1, blank=True, null=True)
    response_code = models.CharField(max_length=4, blank=True, null=True)
    approval_code = models.CharField(max_length=20, blank=True, null=True)
    session_id = models.CharField(max_length=48, blank=True, null=True)
    # others
    mcn = models.CharField(max_length=16, blank=True, null=True)
    verify_id = models.CharField(max_length=30, blank=True, null=True)
    verify_score = models.CharField(max_length=3, blank=True, null=True)
    verify_status = models.CharField(max_length=10, blank=True, null=True)
    currency = models.CharField(max_length=3, blank=True, null=True)
    brand = models.CharField(max_length=10, blank=True, null=True)
    threed_secure_status = models.CharField(max_length=5, blank=True, null=True)
    liability = models.CharField(max_length=10, blank=True, null=True)
    edu_status = models.CharField(max_length=10, blank=True, null=True)
    customer_id = models.CharField(max_length=16, blank=True, null=True)
    token_id = models.CharField(max_length=16, blank=True, null=True)

    def __str__(self):
        return "%s : %s <%s>" % (
            self.created_by,
            self.amount,
            self.transaction_status
        )

    class Meta:
        verbose_name = _("Doku")
        verbose_name_plural = _("Doku")
