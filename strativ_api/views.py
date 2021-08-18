from django.shortcuts import render, redirect, reverse
from rest_framework.views import APIView
from rest_framework.response import Response
import requests # great module for simple http requests and responses

# custom 
from .models import Countries
from .serializers import CountriesSerializer, NeighbouringCountriesSerializer

# Create your views here.
# RESTful APIs
class CollectAPI(APIView):
	def get(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			url = 'https://restcountries.eu/rest/v2/all'
			countries = requests.get(url).json()

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
		
		else:
			return redirect(reverse('home'))


class ListCountries(APIView):
	def get(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			country_list = Countries.objects.all()
			country_list_serializer = CountriesSerializer(instance=country_list, many=True)
			return Response(country_list_serializer.data)

		else:
			return redirect(reverse('home'))


class DetailsCountry(APIView):
	def get(self, request, country_name, *args, **kwargs):
		if request.user.is_authenticated:
			try:
				country_details = Countries.objects.get(name=country_name)
				country_details_serializer = CountriesSerializer(instance=country_details, many=False)
				return Response(country_details_serializer.data)
			except:
				context = {}
				context['NoCountryExists'] = "There is no country named " + country_name
				return Response(context)

		else:
			return redirect(reverse('home'))


class CreateCountry(APIView):
	def post(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			try:
				country_create_serializer = CountriesSerializer(data=request.data)
				if country_create_serializer.is_valid():
					country_create_serializer.save()
					return Response(country_create_serializer.data)
				else:
					context = {}
					context['ValidData'] = 'Please provide valid data'
					return Response(context)
			except: 
				context = {}
				context['ValidData'] = 'Please provide valid data'
				return Response(context)

		else:
			return redirect(reverse('home'))


class UpdateCountry(APIView):   
	def put(self, request, country_name, *args, **kwargs):
		if request.user.is_authenticated:
			try:
				country_update = Countries.objects.get(name=country_name)
				country_update_serializer = CountriesSerializer(instance=country_update,
																data=request.data)
				if country_update_serializer.is_valid():
					country_update_serializer.save()
					return Response(country_update_serializer.data)
				else:
					context = {}
					context['ValidData'] = 'Please provide valid data'
					return Response(context)
			except:
				context = {}
				context['ValidData'] = 'Please provide valid data'
				return Response(context)

		else:
			return redirect(reverse('home'))


class DeleteCountry(APIView):
	def delete(self, request, country_name, *args, **kwargs):
		if request.user.is_authenticated:
			try:
				country_delete = Countries.objects.get(name=country_name)
				country_delete.delete()

				context = {}
				context['Delete'] = 'Successful data deletion'
				return Response(context)
			except:
				context = {}
				context['Delete'] = 'Country named ' + country_name + ' does not exists'
				return Response(context)

		else:
			return redirect(reverse('home'))


class NeighbouringCountries(APIView):
	def get(self, request, country_name, *args, **kwargs):
		if request.user.is_authenticated:
			try:
				countries_neighbouring = Countries.objects.get(name=country_name)
				countries_neighbouring_serializer = NeighbouringCountriesSerializer(instance=countries_neighbouring)
				return Response(countries_neighbouring_serializer.data)
			except:
				context = {}
				context['ValidData'] = 'Please provide valid data'
				return Response(context)

		else:
			return redirect(reverse('home'))


class SameLanguageCountries(APIView):
	def get(self, request, language, *args, **kwargs):
		if request.user.is_authenticated:
			try:
				# To match as last language
				language_last = ' ' + language
				countries_same_language_last = Countries.objects.filter(languages__iendswith=language_last)
				
				# To match as first language
				language_first = language + ','
				countries_same_language_first = Countries.objects.filter(languages__istartswith=language_first)
				
				# To match as middle language
				language_middle = ' ' + language + ','
				countries_same_language_middle = Countries.objects.filter(languages__icontains=language_middle)

				# To match as single language
				countries_same_language_exact = Countries.objects.filter(languages__iexact=language)

				# django style of adding two querysets (| or &)
				countries_same_language = countries_same_language_exact | countries_same_language_first | countries_same_language_last | countries_same_language_middle
		
				countries_same_language_serializer = CountriesSerializer(instance=countries_same_language, many=True)
				return Response(countries_same_language_serializer.data)
			except:
				context = {}
				context['ValidData'] = 'Please provide valid data'
				return Response(context)

		else:
			return redirect(reverse('home'))


class SearchCountry(APIView):
	def get(self, request, country_name, *args, **kwargs):
		if request.user.is_authenticated:
			try:
				# To search partial name as first name of country
				country_search_first = country_name + ' '
				country_search_first = Countries.objects.filter(name__istartswith=country_search_first)
				
				# To search partial name as middle name of country
				country_search_middle = ' ' + country_name + ' '
				country_search_middle = Countries.objects.filter(name__icontains=country_search_middle)
				
				# To search partial name as last name of country
				country_search_last = ' ' + country_name
				country_search_last = Countries.objects.filter(name__iendswith=country_search_last)
				
				# To search exact name of country
				country_search_exact = Countries.objects.filter(name__iexact=country_name)
				
				# django style to add querysets (| or &)
				country_search = country_search_exact | country_search_first | country_search_middle | country_search_last

				country_search_serializer = CountriesSerializer(instance=country_search, many=True)
				return Response(country_search_serializer.data)
			except:
				context = {}
				context['ValidData'] = 'Please provide valid data'
				return Response(context)

		else:
			print('API fail')
			return redirect(reverse('home'))