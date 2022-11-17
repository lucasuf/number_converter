from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework.viewsets import ViewSet


from converter_app.serializers import NumberToEnglishConverterSerializer

number_param = openapi.Parameter(
    "number",
    openapi.IN_QUERY,
    description="number for converting",
    type=openapi.TYPE_INTEGER,
)
user_response = openapi.Response(
    "Response description", NumberToEnglishConverterSerializer
)
# TODO: adjust response to include only number_in_english and status (hint: Schema)


class NumberToEnglishConverterViewSet(ViewSet):
    throttle_classes = [AnonRateThrottle]
    serializer_class = NumberToEnglishConverterSerializer

    @swagger_auto_schema(
        method="get",
        operation_description="GET /number_to_english?number={number}",
        manual_parameters=[number_param],
        responses={200: user_response},
    )
    @swagger_auto_schema(
        method="post",
        operation_description="POST /number_to_english",
        request_body=NumberToEnglishConverterSerializer,
        responses={200: user_response},
    )
    @action(detail=True, methods=["get", "post"])
    def number_to_english(self, request):
        serializer = self.serializer_class(data=request.data or request.query_params)

        if serializer.is_valid():
            return Response(
                {
                    "status": "ok",
                    "number_in_english": serializer.data.get("number_in_english"),
                }
            )
        return Response(
            {"status": "error", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )
