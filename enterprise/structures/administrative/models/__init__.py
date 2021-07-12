import pycountry
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.contrib.gis.db.models import PointField

from enterprise.libs.model import BaseModelGeneric

COUNTRY_CHOICES = [(country.alpha_3, country.name)
                   for country in list(pycountry.countries)]
COUNTRY_KEYS = [country.alpha_3 for country in list(pycountry.countries)]

class Province(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Province')
        verbose_name_plural = _('Provinces')
        ordering = ['name']


class Regency(models.Model):
    province = models.ForeignKey(Province, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Regency')
        verbose_name_plural = _('Regencies')
        ordering = ['name']


class District(models.Model):
    regency = models.ForeignKey(Regency, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    postal_code = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('District')
        verbose_name_plural = _('Districts')
        ordering = ['name']


class Village(models.Model):
    village_code = models.CharField(max_length=20)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    postal_code = models.PositiveIntegerField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Village')
        verbose_name_plural = _('Villages')
        ordering = ['name']


class Address(BaseModelGeneric):
    name = models.CharField(max_length=255)
    address = models.TextField()
    postal_code = models.PositiveIntegerField(null=True, blank=True)
    country = models.CharField(max_length=3, choices=COUNTRY_CHOICES,
                               default='IDN')
    timezone = models.CharField(max_length=48, blank=True, null=True)
    lat_lng = PointField(blank=True, null=True, help_text=_(
        'Locations\'s latitude and longitude'))
    province = models.ForeignKey(
        Province, on_delete=models.CASCADE, blank=True, null=True)
    regency = models.ForeignKey(
        Regency, on_delete=models.CASCADE, blank=True, null=True)
    district = models.ForeignKey(
        District, on_delete=models.CASCADE, blank=True, null=True)
    village = models.ForeignKey(
        Village, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        full_name = self.owned_by.full_name
        address_name = self.name
        return f'{full_name}\'s {address_name}'

    def get_full_address(self):
        regency = self.regency.name if self.regency else None
        province = self.province.name if self.province else None

        full_address = f'{self.address}, {regency}, {province} - {self.postal_code}'

        return full_address