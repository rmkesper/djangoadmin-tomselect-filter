from django.apps import apps
from django.contrib.admin.views.decorators import staff_member_required
from django.core.exceptions import FieldError
from django.db.models import Q
from django.http import JsonResponse


@staff_member_required
def lookup_view(request):
    model_str = request.GET.get("model")
    field = request.GET.get("field")
    mode = request.GET.get("mode", "icontains")
    q = request.GET.get("q", "")

    if not model_str or not field:
        return JsonResponse([], safe=False)

    app_label, model_name = model_str.split(".")
    model = apps.get_model(app_label, model_name)

    queryset = (
        model.objects.values_list(field, flat=True).distinct()
        if "contains" in mode
        else model.objects.all()
    )
    if q:
        filter_set = Q()
        for term in q.split(","):
            filter_set |= Q(**{f"{field}__{mode}": term})
        try:
            queryset = queryset.filter(filter_set)
        except FieldError:
            filter_set = Q()
            for term in q.split(","):
                filter_set |= Q(**{"pk": int(term)})
            queryset = queryset.filter(filter_set)

    results = [
        {"value": str(val) if "contains" in mode else val.pk, "label": str(val)}
        for val in queryset
        if val is not None
    ]
    return JsonResponse(results, safe=False)
