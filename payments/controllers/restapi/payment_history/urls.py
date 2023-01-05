from django.urls import path
from loan_management.urls import (
    URL_READ_ONLY,
    URL_DETAIL,
    URL_CREATE,
    URL_UPDATE,
    URL_DELETE
)

from .api import(
    ApiPublicPaymentHistoryListDetail,
    ApiPrivatePaymentHistoryViewSet
)

VERSION = 'v1'

urlpatterns = [
    # public
    path(
        f'{VERSION}/public/list',
        ApiPublicPaymentHistoryListDetail.as_view(URL_READ_ONLY),
        name='api_public_payment_history_list_detail'
    ),

    # private
    path(
        f'{VERSION}/private/list',
        ApiPrivatePaymentHistoryViewSet.as_view(URL_READ_ONLY),
        name='api_private_payment_history_list_detail'
    ),
    path(
        f'{VERSION}/private/create',
        ApiPrivatePaymentHistoryViewSet.as_view(URL_CREATE),
        name='api_private_payment_history_create'
    ),
    path(
        f'{VERSION}/private/<pk>/update',
        ApiPrivatePaymentHistoryViewSet.as_view(URL_UPDATE),
        name='api_private_payment_history_update'
    ),
    path(
        f'{VERSION}/private/<pk>/delete',
        ApiPrivatePaymentHistoryViewSet.as_view(URL_DELETE),
        name='api_private_payment_history_delete'
    ),
]

"""
Add to urls.py urlpatterns:
    path('payment_history/api/', include('payments.controllers.restapi.payment_history.urls'))
