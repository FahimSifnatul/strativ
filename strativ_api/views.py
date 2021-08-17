from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.
class CollectAPI(APIView):
	def get(self, request, *args, **kwargs):
		return Response(request.GET)
