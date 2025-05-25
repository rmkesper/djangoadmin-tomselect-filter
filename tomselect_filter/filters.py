from django.contrib.admin.filters import FieldListFilter
from django.db.models import QuerySet
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
        """
        return None

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
