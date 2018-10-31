'''
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# File: constants.py
# Project: core.ayopeduli.id
# File Created: Wednesday, 31st October 2018 7:32:35 pm
# 
# Author: Arif Dzikrullah
#         ardzix@hotmail.com>
#         https://github.com/ardzix/>
# 
# Last Modified: Wednesday, 31st October 2018 7:32:35 pm
# Modified By: arifdzikrullah (ardzix@hotmail.com>)
# 
# Peduli sesama, sejahtera bersama
# Copyright - 2018 Ayopeduli.Id, ayopeduli.id
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''


from django.utils.translation import gettext_lazy as _
import pycountry

COUNTRY_CHOICES = [(country.alpha_3, country.name) for country in list(pycountry.countries)]
COUNTRY_KEYS = [country.alpha_3 for country in list(pycountry.countries)]
CURRENCY_CHOICES = [(currency.alpha_3, currency.name) for currency in list(pycountry.currencies)]
LANGUAGE_CHOICES = [(language.alpha_3, language.name) for language in list(pycountry.languages)]

POST_STATUS_CHOICES = (
	('pending', _('Pending')),
	('preparing', _('Preparing')),
	('published', _("Published")),
	('banned', _("Banned")),
)

GENDER_CHOICES = (
    (1, _('Male')),
    (2, _('Female')),
    (3, _('Secret')),
)