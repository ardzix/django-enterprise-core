'''
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# File: decimal_lib.py
# Project: core.ayopeduli.id
# File Created: Thursday, 1st November 2018 1:22:54 am
#
# Author: Arif Dzikrullah
#         ardzix@hotmail.com>
#         https://github.com/ardzix/>
#
# Last Modified: Thursday, 1st November 2018 1:22:54 am
# Modified By: arifdzikrullah (ardzix@hotmail.com>)
#
# Peduli sesama, sejahtera bersama
# Copyright - 2018 Ayopeduli.Id, ayopeduli.id
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''


from decimal import Decimal, ROUND_HALF_UP
TWOPLACES = Decimal(10) ** -2


def round_decimal(number):
    number = Decimal(number)
    return Decimal(number.quantize(Decimal('.01'), rounding=ROUND_HALF_UP))


def dec_to_str(amount_decimal):
    return str(amount_decimal.quantize(TWOPLACES))
