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