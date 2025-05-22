from django.urls import path
from .views import lookup_view

app_name = "tomselect_filter"

urlpatterns = [
    path("lookup/", lookup_view, name="lookup"),
]
