from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from urllib.request import urlopen

# custom 
from .models import Countries

# Create your views here.
class CollectAPI(APIView):
	def get(self, request, *args, **kwargs):
		url = 'https://restcountries.eu/rest/v2/all'
		countries = JSONParser().parse(urlopen(url)) 

		return Response(countries)
