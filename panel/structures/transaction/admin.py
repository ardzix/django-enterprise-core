'''
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# File: admin.py
# Project: core.ayopeduli.id
# File Created: Thursday, 1st November 2018 1:48:05 am
#
# Author: Arif Dzikrullah
#         ardzix@hotmail.com>
#         https://github.com/ardzix/>
#
# Last Modified: Thursday, 1st November 2018 1:48:06 am
# Modified By: arifdzikrullah (ardzix@hotmail.com>)
#
# Peduli sesama, sejahtera bersama
# Copyright - 2018 Ayopeduli.Id, ayopeduli.id
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''


from django.contrib import admin
from .models import *


class WalletAdmin(admin.ModelAdmin):
    pass


class InvoiceAdmin(admin.ModelAdmin):
    pass


class InvoiceItemAdmin(admin.ModelAdmin):
    pass


class TopUpAdmin(admin.ModelAdmin):
    pass


admin.site.register(Wallet, WalletAdmin)
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(InvoiceItem, InvoiceItemAdmin)
admin.site.register(TopUp, TopUpAdmin)
