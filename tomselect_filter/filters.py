from django.contrib.admin import SimpleListFilter
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.db.models import Field


from django.contrib.admin.filters import FieldListFilter

class TomSelectListFilter(FieldListFilter):
    template = "admin/filters/tomselect_filter.html"

    def __init__(self, field, request, params, model, model_admin, field_path):
        self.field = field
        self.model = model
        self.parameter_name = field_path
        self.title = field.verbose_name.title()
        super().__init__(field, request, params, model, model_admin, field_path)

    def expected_parameters(self):
        return [self.parameter_name]

    def choices(self, changelist):
        return []

    def get_title(self):
        return self.title

    def get_lookup_url(self):
        return reverse("tomselect_filter:lookup") + f"?model={self.model._meta.app_label}.{self.model._meta.model_name}&field={self.parameter_name}"
