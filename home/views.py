from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from urllib.request import urlopen, Request

# custom
from strativ_api.models import Countries

# Create your views here.
class Home(APIView):
	def get(self, request, *args, **kwargs):
		context = {}
		context['countries'] = Countries.objects.all()
		return render(request, 'home.html', context)

	def post(self, request, *args, **kwargs):
		if 'search_country_text' in request.POST:
			name = request.POST['search_country_text']
			http_response_object = urlopen('http://127.0.0.1:8000/search-country/'+name)
			
			country = JSONParser().parse(http_response_object)
			if len(country) == 0:
				return HttpResponse("<h1>No country exists with the name '" + name + "'</h1>")

			context = {}
			context['countries'] = country
			return render(request, 'home.html', context)
		else:
			country_name = list(request.POST.items())[0][0] # To retrieve country name from Form name
			country = Countries.objects.get(name=country_name)

			context = {}
			context['name'] = country_name
			context['flag'] = country.flag
			context['borders'] = country.borders
			context['languages'] = country.languages
			
			return render(request, 'details.html', context)