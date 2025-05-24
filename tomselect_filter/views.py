from django.apps import apps
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from django.http import JsonResponse


@staff_member_required
def lookup_view(request):
    model_str = request.GET.get("model")
    field = request.GET.get("field")
    q = request.GET.get("q", "")

    if not model_str or not field:
        return JsonResponse([], safe=False)

    app_label, model_name = model_str.split(".")
    model = apps.get_model(app_label, model_name)

    queryset = model.objects.values_list(field, flat=True).distinct()
    if q:
        filter_set = Q()
        for term in q.split(","):
            filter_set |= Q(**{f"{field}__icontains": term})
        queryset = queryset.filter(filter_set)

    results = [{"value": val, "label": str(val)} for val in queryset]  # TODO limit
    return JsonResponse(results, safe=False)
