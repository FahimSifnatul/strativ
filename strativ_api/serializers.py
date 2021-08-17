from rest_framework import serializers
# custom models
from .models import Countries

class CountriesSerialier(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Countries
		fields = '__all__'