from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response


class ReferenceConstantMixin(GenericViewSet):
    def generate_response(self):
        constant = self.constant
        response = [{"value": i[0], "text": i[1]} for i in constant]

        return response

    def list(self, request):
        response = self.generate_response()

        return Response(response)


class ReferenceModelMixin(GenericViewSet):
    value_text_field = {"value": "id62", "text": "display_name"}

    def list(self, request):
        response = [
            {
                "value": getattr(i, self.value_text_field.get("value")),
                "text": getattr(i, self.value_text_field.get("text")),
            }
            for i in self.queryset
        ]

        return Response(response)
