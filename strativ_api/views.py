from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from urllib.request import urlopen

# custom 
from .models import Countries
from .serializers import CountriesSerializer

# Create your views here.
class CollectAPI(APIView):
	def get(self, request, *args, **kwargs):
		url = 'https://restcountries.eu/rest/v2/all'
		countries = JSONParser().parse(urlopen(url)) 

		check_len = len(Countries.objects.all())
		if check_len == 0: # means collected api data is not yet stored in model
			APIData = []
			for country in countries:
				name 	   = country['name']
				alpha2code = country['alpha2Code']
				capital    = country['capital']
				population = country['population']
				timezones  = country['timezones'][0]
				flag       = country['flag']

				languages  = ''
				for language in country['languages']: # country['languages'] is a dict array
					languages += language['name'] + ', '
				languages  = languages[:-2] # To remove last comma

				borders    = ''
				for border in country['borders']: # country['borders'] is a list
					borders += border + ', '
				borders    = borders[:-2] # To remove last comma

				APIData.append(Countries(name=name,
										alpha2code = alpha2code,
										capital=capital,
										population=population,
										timezones=timezones,
										flag=flag,
										languages=languages,
										borders=borders
						))
			Countries.objects.bulk_create(APIData)

		return Response(countries)
