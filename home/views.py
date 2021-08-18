from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from urllib.request import urlopen, Request

# custom
from strativ_api.models import Countries

# Create your views here.
class Home(APIView):
	def get(self, request, *args, **kwargs):
		context = {}
		if request.user.is_authenticated:
			context['user_authenticated'] = 'true'
		else:
			context['user_authenticated'] = 'false'
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
			if request.user.is_authenticated:
				context['user_authenticated'] = 'true'
			else:
				context['user_authenticated'] = 'false'
			context['countries'] = country
			return render(request, 'home.html', context)
		
		elif 'sign_in_submit' in request.POST: # sign in checking
			username = request.POST['username']
			password = request.POST['password']

			context = {}
			user = authenticate(username=username, password=password)
			if user is not None: # user exists
				login(request, user)
				context['user_authenticated'] = 'true'
				context['countries'] = Countries.objects.all()
			else: # no user exists
				context['user_authenticated'] = 'false'
				messages.error(request, 'Username-Password mismatch or no user exists with username ' + username)
			return render(request, 'home.html', context)

		elif 'sign_up_submit' in request.POST: # sign up checking
			new_username = request.POST['new_username']
			new_password = request.POST['new_password']

		else:
			country_name = list(request.POST.items())[0][0] # To retrieve country name from Form name
			country = Countries.objects.get(name=country_name)

			context = {}
			context['name'] = country_name
			context['flag'] = country.flag
			context['borders'] = country.borders
			context['languages'] = country.languages
			
			return render(request, 'details.html', context)