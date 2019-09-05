'''
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# File: ip_address.py
# Project: core.wecare.id
# File Created: Tuesday, 27th November 2018 3:44:01 am
#
# Author: Arif Dzikrullah
#         ardzix@hotmail.com>
#         https://github.com/ardzix/>
#
# Last Modified: Tuesday, 27th November 2018 3:44:01 am
# Modified By: arifdzikrullah (ardzix@hotmail.com>)
#
# Handcrafted and Made with Love
# Copyright - 2018 Wecare.Id, wecare.id
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip_list = x_forwarded_for.split(',')
        ip = ip_list[len(ip_list) - 2] if len(ip_list) >= 2 else ip_list[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
