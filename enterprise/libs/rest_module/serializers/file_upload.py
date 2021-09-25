from rest_framework import serializers

from enterprise.libs.base64 import decode_base64


class ChunkUploadSerializer(serializers.Serializer):
    file_name = serializers.CharField()
    chunk = serializers.CharField(required=False)
    chunk_no = serializers.IntegerField(required=False)
    checksum = serializers.CharField(required=False)
    chunk_count = serializers.IntegerField(required=False)


class Base64UploadSerializer(serializers.Serializer):
    file_name = serializers.CharField()
    file_base64 = serializers.CharField()

    def validate(self, attrs):
        file_base64 = attrs.get("file_base64")
        try:
            file_data = decode_base64(file_base64)
        except Exception as e:
            raise serializers.ValidationError(
                {"file_base64": "Base64 decoding error: %s" % str(e)}
            )

        attrs["file_data"] = file_data
        return attrs
