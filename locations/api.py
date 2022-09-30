# Create your views here.
from rest_framework import permissions, viewsets, generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from locations import models
from locations import serializers
from locations.models import Region, Province, City, Country
from locations.serializers import ProvinceSerializer, CitySerializer, RegionSerializer, CityCoordinateSerializer


class LargeResultsSetPagination(PageNumberPagination):
  page_size = 1000
  page_size_query_description = 'page_size'
  max_page_size = 10000

class ApiCountryViewSet(viewsets.ModelViewSet):
  """Viewset for the Country Class"""
  queryset = models.Country.objects.all()
  serializer_class = serializers.CountrySerializer
  permission_classes = [permissions.AllowAny]
  pagination_class = LargeResultsSetPagination


class ApiRegionViewSet(viewsets.ModelViewSet):
  """ViewSet for the Region class"""

  queryset = models.Region.objects.all()
  serializer_class = serializers.RegionSerializer
  permission_classes = [permissions.AllowAny]


class ApiProvinceViewSet(viewsets.ModelViewSet):
  """ViewSet for the Province class"""

  queryset = models.Province.objects.all()
  serializer_class = serializers.ProvinceSerializer
  # permission_classes = [permissions.IsAuthenticated]


class ApiCityViewSet(viewsets.ModelViewSet):
  """ViewSet for the City class"""

  queryset = models.City.objects.all()
  serializer_class = serializers.CitySerializer
  # permission_classes = [permissions.IsAuthenticated]


class ProvincesofRegionViewSet(generics.ListAPIView):
  """Viewset for provinces of region"""
  serializer_class = serializers.ProvinceSerializer
  permission_classes = [permissions.AllowAny]

  def get_queryset(self):
    region = self.request.GET.get('region')
    return models.Province.objects.filter(region=region).order_by('name')


class CitiesOfProvinceViewSet(generics.ListAPIView):
  """Viewset for cities of province"""
  serializer_class = serializers.CitySerializer
  permission_classes = [permissions.AllowAny]

  def get_queryset(self):
    province = self.request.GET.get('province')
    return models.City.objects.filter(province=province).order_by('name')


class ApiRegionsByCountry(APIView):
  permission_classes = [permissions.AllowAny]

  def get(self, request, *args, **kwargs):
    """
    Get regions by country id
    ?id=int
    :param request:
    :param args:
    :param kwargs:
    :return:
    """
    country_id = request.GET.get('id', None)
    country = get_object_or_404(Country, id=country_id)

    regions = Region.objects.filter(country=country)

    serializer = RegionSerializer(regions, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


class ApiProvincesByRegion(APIView):
  permission_classes = [permissions.AllowAny]

  def get(self, request, *args, **kwargs):
    """
    Get provinces by region id
    ?id=int
    :param request:
    :param args:
    :param kwargs:
    :return:
    """
    region_id = request.GET.get('id', None)
    region = get_object_or_404(Region, id=region_id)

    provinces = Province.objects.filter(region=region)

    serializer = ProvinceSerializer(provinces, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


class ApiCitiesByProvince(APIView):
  permission_classes = [permissions.AllowAny]

  def get(self, request, *args, **kwargs):
    """
    Get cities by province id
    ?id=int
    :param request:
    :param args:
    :param kwargs:
    :return:
    """
    province_id = request.GET.get('id', None)
    province = get_object_or_404(Province, id=province_id)

    cities = City.objects.filter(province=province)

    serializer = CitySerializer(cities, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)



# class ApiCityCoordinate(APIView):
#   permission_classes = [permissions.AllowAny]
#
#   def get(self, request, *args, **kwargs):
#     """
#     Get city coordiantes of verified users from Philippines
#     :param request:
#     :param args:
#     :param kwargs:
#     :return:
#     """
#     address = ProfileAddress.objects.filter(profile__user__is_verified=True)
#     address = address.exclude(city__isnull=True)
#     coordinates = [c.city.get_coords() for c in address]
#
#     serializer = CityCoordinateSerializer(coordinates, many=True)
#
#     return Response(serializer.data, status=status.HTTP_200_OK)
