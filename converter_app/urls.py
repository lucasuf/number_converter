from django.urls import path
from converter_app.views import NumberToEnglishConverterViewSet


urlpatterns = [
    path(
        route="number_to_english",
        view=NumberToEnglishConverterViewSet.as_view(
            {"get": "number_to_english", "post": "number_to_english"}
        ),
        name="rest_number_to_english_converter",
    ),
]
