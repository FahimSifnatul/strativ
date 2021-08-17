from django.shortcuts import render
from rest_framework.views import APIView

# Create your views here.
class Home(APIView):
	def get(self, request, *args, **kwargs):
		context = {}
		return render(request, 'home.html', context)