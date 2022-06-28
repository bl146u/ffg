from datetime import datetime, timedelta

from rest_framework.filters import BaseFilterBackend
from rest_framework.exceptions import ValidationError


class DateRangeFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        date_from = request.GET.get("from")
        date_to = request.GET.get("to")

        if not date_from or not date_to:
            raise ValidationError({"details": "Введите дату FROM и дату TO"})

        date_from = datetime.fromisoformat(date_from)
        date_to = datetime.fromisoformat(date_to) + timedelta(days=1)

        if date_from >= date_to:
            raise ValidationError({"details": "Дата FROM должна быть меньше даты TO"})

        return queryset.filter(date__gte=date_from, date__lt=date_to)


class DateRangeOneFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        date = request.GET.get("date")
        date_from = request.GET.get("from")
        date_to = request.GET.get("to")

        if not date and (not date_from or not date_to):
            raise ValidationError(
                {"details": "Введите дату FROM и дату TO или дату DATE"}
            )

        if date:
            date_from = date
            date_to = date

        date_from = datetime.fromisoformat(date_from)
        date_to = datetime.fromisoformat(date_to) + timedelta(days=1)

        if date_from >= date_to:
            raise ValidationError({"details": "Дата FROM должна быть меньше даты TO"})

        return queryset.filter(date__gte=date_from, date__lt=date_to)
