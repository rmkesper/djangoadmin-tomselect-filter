from urllib.parse import parse_qs, urlparse

from django.contrib.admin.filters import FieldListFilter
from django.core.exceptions import FieldError
from django.db.models import Q, QuerySet
from django.http import JsonResponse
from django.urls import reverse


class TomSelectListFilter(FieldListFilter):
    template = "admin/filters/tomselect_filter.html"

    def __init__(self, field, request, params, model, model_admin, field_path):
        self.mode = "icontains"
        self.field = field
        self.model = model
        self.parameter_name = field_path
        self.admin_model = model
        self.request = request
        self.title = (
            field.verbose_name.title() if getattr(field, "verbose_name", None) else ""
        )
        super().__init__(field, request, params, model, model_admin, field_path)

    def expected_parameters(self):
        return [self.parameter_name]

    def choices(self, changelist):
        return []

    def get_title(self):
        return self.title

    def get_model(self):
        """The lookup model for reference."""
        return self.model

    def get_admin_model(self):
        """The model for reference to the model admin."""
        return self.admin_model

    def get_custom_queryset(
        self, term=None, queryset=None, admin_query: str | None = None, *args, **kwargs
    ) -> JsonResponse:
        """
        Override the default queryset handling if needed.
        Either use extend queryset OR custom queryset!
        """
        return None

    def get_extend_queryset(
        self, term=None, queryset=None, admin_query: str | None = None, *args, **kwargs
    ) -> QuerySet:
        """
        Extend the default queryset if needed.
        Either use extend queryset OR custom queryset!

        Below gets the queryset for the tomselect options filtered by the current available
        options in the related django admin view. either use super().get_extend_queryset(...)
        to maintain this or override if needed.
        """
        if isinstance(admin_query, str) and queryset:
            query_string = urlparse(admin_query).query
            params = parse_qs(query_string)
            filter_set = Q()
            for k, v in params.items():
                if isinstance(v, list):
                    sub_filterset = Q()
                    for e in v:
                        sub_filterset |= Q(**{f"{k}": e})
                    filter_set &= Q(sub_filterset)
                else:
                    filter_set &= Q(**{f"{k}": v})

            try:
                queryset = queryset.filter(filter_set)
            except (FieldError, LookupError):
                pass
        return queryset

    def get_lookup_url(self):
        app_label = self.get_model()._meta.app_label
        model_name = self.get_model()._meta.model_name
        admin_app_label = self.get_admin_model()._meta.app_label
        admin_model_name = self.get_admin_model()._meta.model_name
        return (
            reverse("tomselect_filter:lookup") + f"?model={app_label}.{model_name}"
            f"&admin_model={admin_app_label}.{admin_model_name}"
            f"&field={self.parameter_name}"
        )
