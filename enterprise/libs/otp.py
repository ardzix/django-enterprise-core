'''
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# File: otp.py
# Project: django-panel-core
# File Created: Tuesday, 25th February 2020 12:57:24 am
# 
# Author: Arif Dzikrullah
#         ardzix@hotmail.com>
#         https://github.com/ardzix/>
# 
# Last Modified: Tuesday, 25th February 2020 12:57:24 am
# Modified By: Arif Dzikrullah (ardzix@hotmail.com>)
# 
# Hand-crafted & Made with Love
# Copyright - 2018 Ardz Co, https://github.com/ardzix/django-panel-core
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''
import random



def generate_otp_code(length):
    """Generate OTP code with custom length

    Arguments:
        length {integer} -- Length of code [Max 6]
    """

    otp = ""
    for i in range(length):
        otp += str(random.randint(1, 9))

    return otp