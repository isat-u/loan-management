from django.urls import path
from loan_management.urls import (
    URL_READ_ONLY,
    URL_DETAIL,
    URL_CREATE,
    URL_UPDATE,
    URL_DELETE
)

from .api import(
    ApiPublicPaymentRequestListDetail,
    ApiPrivatePaymentRequestViewSet
)

VERSION = 'v1'

urlpatterns = [
    # public
    path(
        f'{VERSION}/public/list',
        ApiPublicPaymentRequestListDetail.as_view(URL_READ_ONLY),
        name='api_public_payment_request_list_detail'
    ),

    # private
    path(
        f'{VERSION}/private/list',
        ApiPrivatePaymentRequestViewSet.as_view(URL_READ_ONLY),
        name='api_private_payment_request_list_detail'
    ),
    path(
        f'{VERSION}/private/create',
        ApiPrivatePaymentRequestViewSet.as_view(URL_CREATE),
        name='api_private_payment_request_create'
    ),
    path(
        f'{VERSION}/private/<pk>/update',
        ApiPrivatePaymentRequestViewSet.as_view(URL_UPDATE),
        name='api_private_payment_request_update'
    ),
    path(
        f'{VERSION}/private/<pk>/delete',
        ApiPrivatePaymentRequestViewSet.as_view(URL_DELETE),
        name='api_private_payment_request_delete'
    ),
]

"""
Add to urls.py urlpatterns:
    path('payment_request/api/', include('payments.controllers.restapi.payment_request.urls'))
