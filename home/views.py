from django.shortcuts import render
from rest_framework.views import APIView

# custom
from strativ_api.models import Countries

# Create your views here.
class Home(APIView):
	def get(self, request, *args, **kwargs):
		context = {}
		context['countries'] = Countries.objects.all()
		return render(request, 'home.html', context)

	def post(self, request, *args, **kwargs):
		country_name = list(request.POST.items())[0][0] # To retrieve country name from Form name
		country = Countries.objects.get(name=country_name)

		context = {}
		context['name'] = country_name
		context['flag'] = country.flag
		context['borders'] = country.borders
		context['languages'] = country.languages
		
		return render(request, 'details.html', context)