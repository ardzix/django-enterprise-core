import base64
import uuid
from django.core.files.base import ContentFile


def decode_base64(base64_text, file_name=None):
    format, imgstr = base64_text.split(";base64,")
    ext = format.split("/")[-1]

    if not file_name:
        file_name = str(uuid.uuid4())[:12]
    file_decoded = ContentFile(base64.b64decode(imgstr), name=f"{file_name}.{ext}")

    return file_decoded
