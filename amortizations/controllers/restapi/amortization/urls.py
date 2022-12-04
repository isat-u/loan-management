from django.urls import path
from loan_management.urls import (
    URL_READ_ONLY,
    URL_DETAIL,
    URL_CREATE,
    URL_UPDATE,
    URL_DELETE
)

from .api import(
    ApiPublicAmortizationListDetail,
    ApiPrivateAmortizationViewSet
)

VERSION = 'v1'

urlpatterns = [
    # public
    path(
        f'{VERSION}/public/list',
        ApiPublicAmortizationListDetail.as_view(URL_READ_ONLY),
        name='api_public_amortization_list_detail'
    ),

    # private
    path(
        f'{VERSION}/private/list',
        ApiPrivateAmortizationViewSet.as_view(URL_READ_ONLY),
        name='api_private_amortization_list_detail'
    ),
    path(
        f'{VERSION}/private/create',
        ApiPrivateAmortizationViewSet.as_view(URL_CREATE),
        name='api_private_amortization_create'
    ),
    path(
        f'{VERSION}/private/<pk>/update',
        ApiPrivateAmortizationViewSet.as_view(URL_UPDATE),
        name='api_private_amortization_update'
    ),
    path(
        f'{VERSION}/private/<pk>/delete',
        ApiPrivateAmortizationViewSet.as_view(URL_DELETE),
        name='api_private_amortization_delete'
    ),
]

"""
Add to urls.py urlpatterns:
    path('amortization/api/', include('amortizations.controllers.restapi.amortization.urls'))
