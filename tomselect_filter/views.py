from django.apps import apps
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse


@staff_member_required
def lookup_view(request):
    model_str = request.GET.get("model")
    field = request.GET.get("field")
    q = request.GET.get("q", "")  # TODO multiple values

    if not model_str or not field:
        return JsonResponse([], safe=False)

    app_label, model_name = model_str.split(".")
    model = apps.get_model(app_label, model_name)

    queryset = model.objects.values_list(field, flat=True).distinct()
    if q:
        queryset = queryset.filter(**{f"{field}__icontains": q})

    results = [{"value": val, "label": str(val)} for val in queryset[:20]]  # TODO limit
    return JsonResponse(results, safe=False)
