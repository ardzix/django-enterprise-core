import hashlib
import io
from base64 import b64decode

from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from enterprise.libs.storage import STORAGE_CHUNK
from enterprise.libs.rest_module.response import DRFResponse
from enterprise.structures.common.models import File
from enterprise.structures.integration.models import ChunkedUpload
from enterprise.libs.rest_module.serializers.file_upload import (
    ChunkUploadSerializer,
    Base64UploadSerializer,
)


class ChunkUploadViewSet(GenericViewSet):
    serializer_class = ChunkUploadSerializer
    permission_classes = (IsAuthenticated,)
    file_model_class = File

    def create(self, request):
        """
        Chunk upload file.

        ### Requires
        * __file_name__
        * __chunk__
        * __chunk_no__
        * __checksum__
        * __chunk_count__
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        storage = STORAGE_CHUNK
        chunk = serializer.validated_data.get("chunk")
        file_name = serializer.validated_data.get("file_name")
        chunk_no = serializer.validated_data.get("chunk_no")
        checksum = serializer.validated_data.get("checksum")
        chunk_count = serializer.validated_data.get("chunk_count")

        if request.GET.get("is_init"):
            _data, created = ChunkedUpload.objects.get_or_create(
                created_by=request.user,
                filename=file_name,
            )
            data_response = {"created": created}

        elif request.GET.get("is_checksum"):
            base64_str = ""
            for iterate in range(chunk_count):
                chunk_file_name = file_name + ".part_" + str(iterate)
                chunk_file = storage.open(chunk_file_name, mode="r")
                base64_str += str(chunk_file.read())
                storage.delete(chunk_file_name)

            base64_bytes = base64_str.encode("utf-8")
            hash_md5 = hashlib.md5()
            hash_md5.update(base64_bytes)

            if checksum == hash_md5.hexdigest():
                file = b64decode(base64_str.split(",")[-1])

                with io.BytesIO() as f:
                    f.write(file)
                    storage.save(file_name, f)

                # save to file
                chunk_file = storage.open(file_name)
                file_instance = self.file_model_class.objects.create(
                    created_by=request.user, display_name=file_name
                )
                file_instance.file.save(file_name, chunk_file, save=True)

                # delete chunk file
                storage.delete(file_name)

                response = DRFResponse(
                    {"en": "Success upload file", "id": "Sukses mengunggah file"}
                )
                data = {
                    "url": file_instance.get_safe_url(),
                    "file_id62": file_instance.id62,
                    "file_name": file_instance.display_name,
                }
                return response.get_success_response("200", data)

        else:
            with io.StringIO() as f:
                f.write(chunk)
                storage.save(file_name + ".part_" + str(chunk_no), f)

            data_response = {
                "chunk_no": chunk_no,
            }

        return Response(data_response)


class Base64UploadViewSet(GenericViewSet):
    """
    Upload File by Base64

    ## Body
    - file_name __full file name__ example: picture.jpg
    - file_base64 __base64 file encoded with mimetype. example "data:image/png;base64,iVBORw0KGgoAAAA..." (reference: https://www.base64-image.de)
    """

    serializer_class = Base64UploadSerializer
    permission_classes = (IsAuthenticated,)
    file_model_class = File

    def get_response(self, file_instance):
        response = DRFResponse(
            {"en": "Success upload file", "id": "Sukses mengunggah file"}
        )
        data = {
            "url": file_instance.get_safe_url(),
            "file_id62": file_instance.id62,
            "file_name": file_instance.display_name,
        }
        return response.get_success_response("200", data)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        file_data = serializer.validated_data.get("file_data")
        file_name = serializer.validated_data.get("file_name")

        file_instance = self.file_model_class.objects.create(
            display_name=file_name, file=file_data, created_by=request.user
        )

        return self.get_response(file_instance)
