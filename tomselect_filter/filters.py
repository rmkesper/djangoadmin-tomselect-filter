from django.contrib.admin.filters import FieldListFilter
from django.urls import reverse


class TomSelectListFilter(FieldListFilter):
    template = "admin/filters/tomselect_filter.html"

    def __init__(self, field, request, params, model, model_admin, field_path):
        self.mode = "icontains"
        self.field = field
        self.model = model
        self.parameter_name = field_path
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
        return self.model

    def get_lookup_url(self):
        app_label = self.get_model()._meta.app_label
        model_name = self.get_model()._meta.model_name
        return (
            reverse("tomselect_filter:lookup")
            + f"?model={app_label}.{model_name}&field={self.parameter_name}"
        )
