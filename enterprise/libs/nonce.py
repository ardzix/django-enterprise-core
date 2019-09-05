'''
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# File: nonce.py
# Project: core.lakon.app
# File Created: Friday, 14th September 2018 6:22:02 pm
#
# Author: Arif Dzikrullah
#         ardzix@hotmail.com>
#         https://github.com/ardzix/>
#
# Last Modified: Friday, 14th September 2018 6:22:02 pm
# Modified By: arifdzikrullah (ardzix@hotmail.com>)
#
# Hand-crafted & Made with Love
# Copyright - 2018 Lakon, lakon.app
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''


class NonceObject(object):
    MODEL = None
    NONCE = None
    OBJ = None

    def __init__(self, *args, **kwargs):
        self.MODEL = kwargs.get("model")
        self.NONCE = kwargs.get("nonce")
        obj = self.MODEL.objects.filter(nonce=self.NONCE).first()
        if not obj:
            obj = self.MODEL(nonce=self.NONCE)
        self.OBJ = obj

    def get_instance(self):
        return self.OBJ

    def is_exist(self):
        if self.OBJ.id:
            return True
        else:
            return False
