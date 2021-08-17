"""strativ URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

# custom views
from strativ_api.views import CollectAPI, ListCountries, DetailsCountry, \
                              CreateCountry, UpdateCountry, DeleteCountry

urlpatterns = [
    path('collect-api/', CollectAPI.as_view(), name='collect-api'),
    path('list-countries/', ListCountries.as_view(), name='list-countries'),
    path('details-country/<country_name>', DetailsCountry.as_view(), name='details-country'),
    path('create-country/', CreateCountry.as_view(), name='create-country'),
    path('update-country/<country_name>', UpdateCountry.as_view(), name='update-country'),
    path('delete-country/<country_name>', DeleteCountry.as_view(), name='delete-country'),
    path('admin/', admin.site.urls),
]
