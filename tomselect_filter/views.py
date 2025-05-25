from django.apps import apps
from django.contrib.admin.views.decorators import staff_member_required
from django.core.exceptions import FieldError
from django.db.models import Q
from django.http import JsonResponse


@staff_member_required
def lookup_view(request):
    model_str = request.GET.get("model")
    field = request.GET.get("field")
    q = request.GET.get("q", "")
    is_pk_field = (
        field.endswith("pk")
        or field.endswith("pk__in")
        or field.endswith("id")
        or field.endswith("id__in")
    )

    if not model_str or not field:
        return JsonResponse([], safe=False)

    app_label, model_name = model_str.split(".")
    model = apps.get_model(app_label, model_name)

    queryset = (
        model.objects.all()
        if is_pk_field
        else model.objects.values_list(field, flat=True).distinct()
    )
    filter_spec = "" if is_pk_field else "__icontains"
    if q:
        filter_set = Q()
        for term in q.split(","):
            filter_set |= Q(**{f"{field}{filter_spec}": term})
        try:
            queryset = queryset.filter(filter_set)
        except FieldError:
            pass

    results = [
        {"value": val.pk if is_pk_field else str(val), "label": str(val)}
        for val in queryset
        if val is not None
    ]
    return JsonResponse(results, safe=False)
