from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
import logging


# Create your views here.
class SimpleView(APIView):
    def __init__(self):
        self.logger=logging.getLogger(__name__)
    def get(self, request, *args, **kwargs):
        # query_param = request.GET.get("param")
        # body_param = request.data.get("body_param")
        self.logger.info('hit')
        return Response("Hello, World", status=200)
