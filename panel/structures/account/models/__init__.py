from django.db import models
from django.utils.text import slugify
from django.contrib.gis.db import models as geo
from django.utils.translation import gettext_lazy as _

from core.libs import constant
from core.libs import storage
from core.structures.authentication.models import LakonUser as User
from core.structures.common.models.base import BaseModelGeneric, BaseModelUnique


class UserType(BaseModelGeneric):
    """
    user type: basic, verified, premium, expert, public figure, etc
    """
    display_name = models.CharField(max_length=100,)
    short_name = models.CharField(max_length=100,)

    def __str__(self):
        return self.display_name

    def save(self, *args, **kwargs):
        if self.display_name:
            self.short_name = slugify(self.display_name)
        return super(UserType, self).save(*args, **kwargs)


class Profile(BaseModelUnique):
    type = models.ManyToManyField(UserType)
    country = models.CharField(max_length=3, choices=constant.COUNTRY_CHOICES, 
                                                blank=True, null=True)
    gender = models.PositiveIntegerField(choices=constant.GENDER_CHOICES,
                                                             default=3)
    bio = models.TextField(blank=True, null=True)
    background_cover = models.ImageField(
        storage = storage.STORAGE_USER_COVER,
        max_length=300,
        blank = True,
        null = True
    )
    avatar = models.ImageField(
        storage = storage.STORAGE_USER_AVATAR,
        max_length=300,
        blank = True,
        null = True
    )

    def __str__(self):
        return self.owned_by.stage_name


class Role(BaseModelGeneric):
    """
    role : Camera, script, actor, etc
    """
    display_name = models.CharField(max_length=100,)
    short_name = models.CharField(max_length=100,)

    def __str__(self):
        return self.display_name

    def save(self, *args, **kwargs):
        if self.display_name:
            self.short_name = slugify(self.display_name)
        super(Role, self).save(*args, **kwargs)


class Address(BaseModelGeneric):
    name = models.CharField(max_length=40)
    address = models.TextField()
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=3, choices=constant.COUNTRY_CHOICES)
    timezone = models.CharField(max_length=48, blank=True, null=True)
    point = geo.PointField(blank=True, null=True)

    def __unicode__(self):
        return self.address

    class Meta:
        verbose_name = _("Address")
        verbose_name_plural = _("Addresses")


class Phone(BaseModelGeneric):
    name = models.CharField(max_length=40)
    number = models.CharField(max_length=24)
    country = models.CharField(max_length=3, choices=constant.COUNTRY_CHOICES)
    is_available = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    def __unicode__(self):
        return self.number

    def save(self, *args, **kwargs):
        return super(Phone, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _("Phone")
        verbose_name_plural = _("Phones")


class Company(BaseModelUnique):
    staffs = models.ManyToManyField(User, blank=True)
    address = models.ManyToManyField(Address)
    phone = models.ManyToManyField(Phone)
    country = models.CharField(max_length=3, choices=constant.COUNTRY_CHOICES)
    logo = models.ImageField(
        storage = storage.STORAGE_COMPANY_LOGO,
        max_length=300,
        blank = True,
        null = True
    )
    display_name = models.CharField(max_length=100)
    short_name = models.SlugField(max_length=100)

    def __unicode__(self):
        return self.display_name

    class Meta:
        verbose_name = _("Company")
        verbose_name_plural = _("Companies")


class Brand(BaseModelGeneric):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True, null=True)
    type = models.PositiveIntegerField(choices=constant.BRAND_CHOICES)
    executive = models.ForeignKey(User, on_delete=models.CASCADE, 
                            related_name="%(app_label)s_%(class)s_executive")
    staffs = models.ManyToManyField(User, blank=True)
    address = models.ManyToManyField(Address)
    phone = models.ManyToManyField(Phone)
    country = models.CharField(max_length=3, choices=constant.COUNTRY_CHOICES)
    logo = models.ImageField(
        storage = storage.STORAGE_BRAND_LOGO,
        max_length=300,
        blank = True,
        null = True
    )
    cover = models.ImageField(
        storage = storage.STORAGE_BRAND_COVER,
        max_length=300,
        blank = True,
        null = True
    )
    website_url = models.URLField(blank=True, null=True)
    description = models.CharField(max_length=300, blank=True, null=True)
    display_name = models.CharField(max_length=100)
    short_name = models.SlugField(max_length=100)
    is_product_integrated = models.BooleanField(default=False)
    is_transaction_integrated = models.BooleanField(default=False)
    code = models.CharField(max_length=5, blank=True, null=True)

    def __unicode__(self):
        return self.display_name

    def is_executive(self, user):
        return self.executive.pk == user.pk

    def is_staff(self, user):
        return user.id in self.staffs.values_list("id", flat=True)

    # def get_logo(self):
    #     if self.logo:
    #         return self.logo.url
    #     else:
    #         return NO_IMAGE_URL

    # def get_cover(self):
    #     if self.cover:
    #         return self.cover.url
    #     else:
    #         return NO_IMAGE_URL

    # def get_campaign_link(self):
    #     if self.short_name in BRAND_CAMPAIGN_LINK:
    #         return BRAND_CAMPAIGN_LINK[self.short_name]
    #     else:
    #         return None

    def get_verified_phone(self):
        return self.phone.filter(is_verified=True, is_available=True)

    def get_manager(self):
        from ....libs.brand import BrandManager
        return BrandManager(instance=self)


    class Meta:
        verbose_name = _("Brand")
        verbose_name_plural = _("Brands")


class ResumeHistory(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "%s last login by %s" % (self.created_by.stage_name, 
                                            str(self.created_at))

    class Meta:
        ordering = ['-created_at',]

