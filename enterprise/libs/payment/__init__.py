'''
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# File: __init__.py
# Project: core.wecare.id
# File Created: Monday, 7th January 2019 10:15:02 pm
# 
# Author: Arif Dzikrullah
#         ardzix@hotmail.com>
#         https://github.com/ardzix/>
# 
# Last Modified: Monday, 7th January 2019 10:15:03 pm
# Modified By: arifdzikrullah (ardzix@hotmail.com>)
# 
# Handcrafted and Made with Love
# Copyright - 2018 Wecare.Id, wecare.id
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''


from .midtrans import Gopay, BankTransfer, MandiriEChannel, CreditCard, Snap

class PaymentManager(object):
    channel = 'wallet'
    channel_manager = None

    def __init__(self, channel=None, *args, **kwargs):
        if channel:
            self.channel = channel

        if channel == 'gopay':
            self.channel_manager = Gopay(
                callback_url=kwargs.get('callback_url'), 
                invoice=kwargs.get('invoice')
            )
        elif channel == 'permata' or channel == 'bca' or channel == 'bni':
            self.channel_manager = BankTransfer(
                invoice=kwargs.get('invoice'),
                bank=channel
            )
        elif channel == 'mandiri':
            self.channel_manager = MandiriEChannel(invoice=kwargs.get('invoice'))
        elif channel == 'credit_card':
            self.channel_manager = CreditCard(
                invoice=kwargs.get('invoice'),
                card=kwargs.get('card'),
            )
        elif channel == 'wallet':
            from ..wallet import WalletChannelManager
            self.channel_manager = WalletChannelManager(invoice=kwargs.get('invoice'))
        elif channel == 'snap':
            self.channel_manager = Snap(
                invoice=kwargs.get('invoice'), 
                payment_channel=kwargs.get('payment_channel')
            )
        else:
            raise Exception("Channel not available")

    def get_channel_manager(self):
        return self.channel_manager