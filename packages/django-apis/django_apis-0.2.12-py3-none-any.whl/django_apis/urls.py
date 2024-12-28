from django.urls import path
from django.conf import settings

from . import swagger_ui
from .constants import DJANGO_APIS_SWAGGER_UI_PATH_KEY

DJANGO_APIS_SWAGGER_UI_PATH = getattr(
    settings,
    DJANGO_APIS_SWAGGER_UI_PATH_KEY,
    "docs/",
)
if DJANGO_APIS_SWAGGER_UI_PATH.startswith("/"):
    DJANGO_APIS_SWAGGER_UI_PATH = DJANGO_APIS_SWAGGER_UI_PATH[1:]
if not DJANGO_APIS_SWAGGER_UI_PATH.endswith("/"):
    DJANGO_APIS_SWAGGER_UI_PATH += "/"

urlpatterns = [
    path(
        f"{DJANGO_APIS_SWAGGER_UI_PATH}",
        swagger_ui.swagger_ui_view,
        name="django_apis_swagger_ui_view",
    ),
    path(
        f"{DJANGO_APIS_SWAGGER_UI_PATH}init.js",
        swagger_ui.swagger_ui_init_js,
        name="django_apis_swagger_ui_init_js",
    ),
    path(
        f"{DJANGO_APIS_SWAGGER_UI_PATH}data.json",
        swagger_ui.swagger_ui_data,
        name="django_apis_swagger_ui_data",
    ),
]
