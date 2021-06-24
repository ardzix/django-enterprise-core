from datetime import datetime
from dateutil.relativedelta import relativedelta

from django.db.models import Count, Sum, functions as F

from rest_framework.viewsets import GenericViewSet, mixins
from rest_framework.response import Response

from .filters import StartDateFilterBackend, EndDateFilterBackend, PeriodeFilterBackend


class DateRangeViewSet(GenericViewSet, mixins.ListModelMixin):
    filter_field = "updated_at"
    filter_backends = (StartDateFilterBackend, EndDateFilterBackend)

    def get_queryset_filtered(
        self, start_date=None, end_date=None, date_field=None, queryset=None
    ):
        queryset = queryset if queryset else self.get_queryset()

        start_date = self.request.query_params.get("start_date", start_date)
        end_date = self.request.query_params.get("end_date", end_date)

        filter_field = date_field if date_field else self.filter_field

        if start_date:
            queryset = queryset.filter(**{f"{filter_field}__gte": start_date})

        if end_date:
            queryset = queryset.filter(**{f"{filter_field}__lte": end_date})

        return queryset

    def list(self, request):
        queryset = self.get_queryset_filtered()

        self.queryset = queryset
        return super().list(request)


class PeriodeStatisticViewSet(DateRangeViewSet):
    filter_backends = (
        PeriodeFilterBackend,
        StartDateFilterBackend,
        EndDateFilterBackend,
    )

    def generate_value_annotate(self, field_to_sum=None):
        kword_argument = {"value": Count("id")}
        if field_to_sum:
            kword_argument = {"value": Sum(field_to_sum)}

        return kword_argument

    def get_daily_response(self, field_to_sum=None, filter_field=None, queryset=None):
        queryset = queryset if queryset else self.queryset
        filter_field = filter_field if filter_field else self.filter_field
        return (
            queryset.extra({"date": f"date_trunc('day', {filter_field})"})
            .values("date")
            .annotate(**self.generate_value_annotate(field_to_sum))
            .order_by("date")
        )

    def get_monthly_response(self, field_to_sum=None, filter_field=None, queryset=None):
        queryset = queryset if queryset else self.queryset
        filter_field = filter_field if filter_field else self.filter_field
        return (
            queryset.annotate(date=F.TruncMonth(filter_field))
            .values("date")
            .annotate(**self.generate_value_annotate(field_to_sum))
            .order_by("date")
        )

    def list(self, request):
        queryset = self.get_queryset_filtered()
        self.queryset = queryset

        periode = self.request.query_params.get("periode", "daily")
        if periode == "monthly":
            response = self.get_monthly_response()
        else:
            response = self.get_daily_response()

        return Response(response)


class FullMonthlyViewSet(GenericViewSet):
    filter_field = "created_at"

    def generate_monthly(self, request):
        month_length = self.request.query_params.get("month_length", 12)
        queryset = self.queryset

        today = datetime.today().date()
        response_dict = []
        for month in range(month_length + 1):
            current_date = today - relativedelta(months=month)

            filter_kwargs = {
                f"{self.filter_field}__month": current_date.month,
                f"{self.filter_field}__year": current_date.year,
            }
            value = queryset.filter(**filter_kwargs).count()

            response_dict.append({"date": current_date.replace(day=1), "value": value})

        return response_dict

    def list(self, request):
        return Response(self.generate_monthly(request))
