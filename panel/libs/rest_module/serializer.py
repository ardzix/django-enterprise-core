'''
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# File: serializer.py
# Project: core.lakon.app
# File Created: Friday, 14th September 2018 6:13:56 pm
#
# Author: Arif Dzikrullah
#         ardzix@hotmail.com>
#         https://github.com/ardzix/>
#
# Last Modified: Friday, 14th September 2018 6:14:13 pm
# Modified By: arifdzikrullah (ardzix@hotmail.com>)
#
# Hand-crafted & Made with Love
# Copyright - 2018 Lakon, lakon.app
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''
import timeago
from datetime import timedelta
from rest_framework.serializers import ModelSerializer, ValidationError, SerializerMethodField
from ..nonce import NonceObject


class CommonSerializer(object):
    created_at = SerializerMethodField()
    published_at = SerializerMethodField()
    deleted_at = SerializerMethodField()
    point = SerializerMethodField()

    def get_created_at(self, obj):
        if obj.created_at:
            return {
                'utc': obj.created_at,
                'timestamp': obj.created_at_timestamp,
                'timeago': timeago.format(obj.created_at.replace(tzinfo=None) + timedelta(hours=7))
            }
        return None

    def get_published_at(self, obj):
        if obj.published_at:
            return {
                'utc': obj.published_at,
                'timestamp': obj.published_at_timestamp,
                'timeago': timeago.format(obj.published_at.replace(tzinfo=None) + timedelta(hours=7))
            }
        return None

    def get_deleted_at(self, obj):
        if obj.deleted_at:
            return {
                'utc': obj.deleted_at,
                'timestamp': obj.deleted_at_timestamp,
                'timeago': timeago.format(obj.deleted_at.replace(tzinfo=None) + timedelta(hours=7))
            }
        return None

    def get_point(self, obj):
        point = obj.point
        result = {'latitude': 0, 'longitude': 0}
        try:
            result = {
                'latitude': point.y,
                'longitude': point.x
            }
        except BaseException:
            pass

        return result


class LakonModelSerializer(ModelSerializer):
    def create(self, validated_data):
        if 'nonce' not in validated_data:
            raise ValidationError({'detail': 'Please provide nonce'})

        nonce = validated_data['nonce']
        model = self.Meta.model
        no = NonceObject(model=model, nonce=nonce)

        validated_data['created_by'] = self.context.get('request').user

        if no.is_exist():
            return super(LakonModelSerializer, self).update(
                no.get_instance(), validated_data)
        else:
            return super(LakonModelSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        if 'nonce' not in validated_data:
            raise ValidationError({'detail': 'Please provide nonce'})

        nonce = validated_data['nonce']
        model = self.Meta.model
        no = NonceObject(model=model, nonce=nonce)

        if not no.get_instance() == self.instance:
            raise ValidationError({'detail': 'Nonce is not matched'})

        return super(LakonModelSerializer, self).update(
            self.instance, validated_data)
