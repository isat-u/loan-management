from django.urls import path

from .api import ApiCountryViewSet, ApiRegionViewSet, ApiProvinceViewSet, ApiCityViewSet, ApiProvincesByRegion, \
  ApiCitiesByProvince, ApiRegionsByCountry

version = 'api/v1'

READ_ONLY = {
  'get': 'list'
}

urlpatterns = [
  path(f'{version}/regions_by_country', ApiRegionsByCountry.as_view(), name='regions_by_country'),
  path(f'{version}/provinces_by_region', ApiProvincesByRegion.as_view(), name='provinces_by_region'),
  path(f'{version}/cities_by_province', ApiCitiesByProvince.as_view(), name='cities_by_province'),

  path(f'{version}/countries', ApiCountryViewSet.as_view(READ_ONLY), name='api_location_country_list'),
  path(f'{version}/regions', ApiRegionViewSet.as_view(READ_ONLY), name='api_location_region_list'),
  path(f'{version}/provinces', ApiProvinceViewSet.as_view(READ_ONLY), name='api_location_province_list'),
  path(f'{version}/cities', ApiCityViewSet.as_view(READ_ONLY), name='api_location_city_list'),
]
