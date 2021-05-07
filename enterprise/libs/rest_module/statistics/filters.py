import coreapi
from rest_framework.filters import SearchFilter


class StartDateFilterBackend(SearchFilter):
    def get_schema_fields(self, view):
        return [
            coreapi.Field(
                name="start_date",
                location="query",
                required=False,
                type="date",
                description="filter by start_date",
            )
        ]


class EndDateFilterBackend(SearchFilter):
    def get_schema_fields(self, view):
        return [
            coreapi.Field(
                name="end_date",
                location="query",
                required=False,
                type="date",
                description="filter by end_date",
            )
        ]


class PeriodeFilterBackend(SearchFilter):
    def get_schema_fields(self, view):
        return [
            coreapi.Field(
                name="periode",
                location="query",
                required=True,
                type="string",
                description="filter periode",
            )
        ]


class AggregateFilterBackend(SearchFilter):
    def get_schema_fields(self, view):
        return [
            coreapi.Field(
                name="aggregate",
                location="query",
                required=False,
                type="string",
                description="aggregate type",
            )
        ]


class FieldFilterBackend(SearchFilter):
    def get_schema_fields(self, view):
        return [
            coreapi.Field(
                name="field",
                location="query",
                required=False,
                type="string",
                description="aggregate field",
            )
        ]


class StatusFilterBackend(SearchFilter):
    def get_schema_fields(self, view):
        return [
            coreapi.Field(
                name="status",
                location="query",
                required=False,
                type="string",
                description="filter by status",
            )
        ]
