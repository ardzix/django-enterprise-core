'''
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# File: brand.py
# Project: django-enterprise-core
# File Created: Tuesday, 21st August 2018 11:51:25 pm
#
# Author: Arif Dzikrullah
#         ardzix@hotmail.com>
#         https://github.com/ardzix/>
#
# Last Modified: Friday, 26th October 2018 3:45:31 pm
# Modified By: arifdzikrullah (ardzix@hotmail.com>)
#
# Hand-crafted & Made with Love
# Copyright - 2018 Ardz Co, https://github.com/ardzix/django-enterprise-core
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''
from django.db.models import Q


class BrandManager(object):
    instance = None
    brands = []

    def __init__(self, *args, **kwargs):
        if kwargs.get('instance'):
            self.set_by_instance(kwargs.get('instance'))
        if kwargs.get('owner'):
            self.set_by_owner(kwargs.get('owner'))
        if kwargs.get('executive'):
            self.set_by_executive(kwargs.get('executive'))
        if kwargs.get('staff'):
            self.set_by_staff(kwargs.get('staff'))
        if kwargs.get('user'):
            self.set_by_user(kwargs.get('user'))

    def set_by_instance(self, instance):
        self.brands.append(instance)
        self.change_instance()

    def set_by_owner(self, owner):
        self.brands = self.brand_objects().filter(owned_by=owner).all()
        self.change_instance()

    def set_by_executive(self, executive):
        self.brands = self.brand_objects().filter(executive=executive).all()
        self.change_instance()

    def set_by_staff(self, staff):
        self.brands = self.brand_objects().filter(staffs=staff).all()
        self.change_instance()

    def set_by_user(self, user):
        self.brands = self.brand_objects().filter(
            Q(owned_by=user) | Q(executive=user) | Q(staffs=user)
        ).all()
        self.change_instance()

    def change_instance(self, index=0, request=None):
        if len(self.brands) <= index:
            return False

        self.instance = self.brands[index]
        if request:
            request.session['brand'] = self.instance
            return request

        return True

    def get_brands(self):
        return self.brands

    def get_staffs(self):
        if not self.instance:
            raise Exception("No instance specified")

        return self.instance.staffs.all()

    def get_owner(self):
        if not self.instance:
            raise Exception("No instance specified")

        return self.instance.owned_by

    def get_executive(self):
        if not self.instance:
            raise Exception("No instance specified")

        return self.instance.executive

    def get_company(self):
        if not self.instance:
            raise Exception("No instance specified")

        return self.instance.company

    def get_company_staffs(self):
        if not self.instance:
            raise Exception("No instance specified")

        return self.get_company().staffs.all() if self.get_company() else []

    def get_company_owner(self):
        if not self.instance:
            raise Exception("No instance specified")

        return self.get_company().owned_by if self.get_company() else None

    def is_staff(self, user):
        return True if user in self.get_staffs() else False

    def is_executive(self, user):
        return True if user == self.get_executive() else False

    def is_owner(self, user):
        return True if user == self.get_owner() else False

    def is_company_staff(self, user):
        return True if user in self.get_company_staffs() else False

    def is_company_owner(self, user):
        return True if user == self.get_company_owner() else False

    def get_permissions(self, user):
        if not self.instance:
            raise Exception("No instance specified")

        permissions = []
        if self.is_staff(user):
            permissions.append('staff')
        if self.is_executive(user):
            permissions.append('executive')
        if self.is_owner(user):
            permissions.append('owner')
        return permissions

    def get_company_permissions(self, user):
        if not self.instance:
            raise Exception("No instance specified")

        permissions = []
        if self.is_company_staff(user):
            permissions.append('staff')
        if self.is_company_owner(user):
            permissions.append('owner')
        return permissions
