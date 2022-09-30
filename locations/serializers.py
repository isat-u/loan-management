from . import models
from rest_framework import serializers


class CountrySerializer(serializers.ModelSerializer):
  class Meta:
    model = models.Country
    fields = (
      'pk',
      'iso',
      'name',
      'nicename',
      'iso3',
      'numcode',
      'phonecode'
    )


class RegionSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.Region
    fields = (
      'pk',
      'name',
    )


class ProvinceSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.Province
    fields = (
      'pk',
      'name',
    )


class CitySerializer(serializers.ModelSerializer):
  class Meta:
    model = models.City
    fields = (
      'pk',
      'name'
    )


class CityCoordinateSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.CityCoordinate
    fields = (
      'lat',
      'lon',
    )