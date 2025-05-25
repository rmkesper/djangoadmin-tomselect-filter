from django.apps import apps
from django.contrib.admin import site as admin_site
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.admin.views.main import ChangeList
from django.core.exceptions import FieldError
from django.db.models import Q
from django.http import JsonResponse


@staff_member_required
def lookup_view(request):
    custom_params = {"model", "field", "q", "admin_model"}
    model_str = request.GET.get("model")
    admin_model_str = request.GET.get("admin_model")
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
    admin_app_label, admin_model_name = admin_model_str.split(".")
    model = apps.get_model(app_label, model_name)
    model_admin = admin_site._registry[model]
    admin_model = model
    admin_model_admin = model_admin
    # we need to pass the fitting model admin to dynamically identify where the custom queryset is registered
    if model_str != admin_model_str and "." in admin_model_str:
        admin_model = apps.get_model(admin_app_label, admin_model_name)
        admin_model_admin = admin_site._registry[admin_model]

    # custom queryset defined on filter class

    # remove all custom GET parameters we need for the tomselect filtering
    filtered_get = request.GET.copy()
    for param in custom_params:
        if param in filtered_get:
            del filtered_get[param]

    # Replace GET with cleaned version
    request.GET = filtered_get

    # initialize a changelist to access filters
    cl = ChangeList(
        request,
        admin_model,
        admin_model_admin.list_display,
        admin_model_admin.list_display_links,
        admin_model_admin.list_filter,
        admin_model_admin.date_hierarchy,
        admin_model_admin.search_fields,
        admin_model_admin.list_select_related,
        admin_model_admin.list_per_page,
        admin_model_admin.list_max_show_all,
        admin_model_admin.list_editable,
        admin_model_admin,
        admin_model_admin.sortable_by,
        admin_model_admin.search_help_text,
    )

    for filter_spec in cl.filter_specs:
        if getattr(filter_spec, "parameter_name", None) == field:
            if hasattr(filter_spec, "get_custom_queryset"):
                response = filter_spec.get_custom_queryset(q)
                if response is not None and isinstance(response, JsonResponse):
                    return response

    # default query handling by parameter name
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
        # check if we should return ID or str for the value
        {"value": val.pk if is_pk_field else str(val), "label": str(val)}
        for val in queryset
        if val is not None
    ]
    return JsonResponse(results, safe=False)
