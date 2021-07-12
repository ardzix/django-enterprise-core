import coreapi
from rest_framework.filters import BaseFilterBackend, SearchFilter


class SearchFilterBackend(SearchFilter):
    def get_schema_fields(self, view):
        return [coreapi.Field(
            name='search',
            location='query',
            required=False,
            type='string',
            description='Search by name or description'
        )]


class CategoryFilterBackend(SearchFilter):
    def get_schema_fields(self, view):
        return [coreapi.Field(
            name='category',
            location='query',
            required=False,
            type='string',
            description='Search by category short name'
        )]


class ViewAtFilterBackend(SearchFilter):
    def get_schema_fields(self, view):
        return [coreapi.Field(
            name='is_viewed',
            location='query',
            required=False,
            type='boolean',
            description='Filter by status view'
        )]
