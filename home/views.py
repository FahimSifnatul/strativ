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
			user = authenticate(request, username=username, password=password)
			if user is not None: # user exists - ready to login
				login(request, user)
				context['user_authenticated'] = 'true'
				context['countries'] = Countries.objects.all()
			else: # no user exists
				context['user_authenticated'] = 'false'
				messages.error(request, 'Hey ' + username + ', we appreciate your login try. But would you please check your username and password once more?')
			return render(request, 'home.html', context)

		elif 'sign_up_submit' in request.POST: # sign up checking
			new_username = request.POST['new_username']
			new_email    = request.POST['new_email']
			new_password = request.POST['new_password']

			context = {}
			try: # if successful then already a user exists with requested username/email
				username_checking = len(User.objects.get(username=new_username))
				email_checking 	  = len(User.objects.get(email=new_email))
				existence = ['email', 'username']
				messages.error(request, 'Requested ' + existence[username_checking] + ' already exists')
				context['user_authenticated'] = 'false'
			
			except: # DoesNotExist error means no user exists with requested username & password. Safe to proceed
				new_user = User.objects.create_user(username=new_username, 
													email=new_email,
													password=new_password)
				new_user.save()
				user = authenticate(request,username=new_username,
											password=new_password)
				if user is not None: # user exists - ready to login
					login(request, user)
					context['user_authenticated'] = 'true'
					context['countries'] = Countries.objects.all()
					messages.success(request, 'Congratulations ' + new_username + '!!! You are now a member of our Countries!!! family')
				else: # new user vanished from database 
					context['user_authenticated'] = 'false'
					messages.error(request, 'Hurry ' + new_username + '.... Your account has been deleted by someone from database...')
			
			return render(request, 'home.html', context)

		else:
			print(request.POST)
			country_name = list(request.POST.items())[1][0] # To retrieve country name from Form name
			country = Countries.objects.get(name=country_name)

			context = {}
			context['name'] = country_name
			context['flag'] = country.flag
			context['borders'] = country.borders
			context['languages'] = country.languages
			
			return render(request, 'details.html', context)