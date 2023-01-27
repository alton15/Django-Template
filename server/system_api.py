import os
import time
from datetime import datetime

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.renderers import JSONOpenAPIRenderer

from rest_framework.response import Response


class HealthCheck(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = [JSONOpenAPIRenderer]

    def get(self, request):
        return Response(
            status=200,
            data={
                'code': 200,
                'message': 'server is Healthy.',
                'payload': {
                    "server_time": str(datetime.now()),
                    "server_timezone": [
                        os.environ['TZ'],
                        time.tzname[0]
                    ]
                }
            }
        )
