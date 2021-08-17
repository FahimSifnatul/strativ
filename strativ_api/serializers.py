from rest_framework import serializers
# custom models
from .models import Countries

class CountriesSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Countries
		fields = '__all__'