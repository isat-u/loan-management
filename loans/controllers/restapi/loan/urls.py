from django.urls import path
from loan_management.urls import (
    URL_READ_ONLY,
    URL_DETAIL,
    URL_CREATE,
    URL_UPDATE,
    URL_DELETE
)

from .api import(
    ApiPublicLoanListDetail,
    ApiPrivateLoanViewSet
)

VERSION = 'v1'

urlpatterns = [
    # public
    path(
        f'{VERSION}/public/list',
        ApiPublicLoanListDetail.as_view(URL_READ_ONLY),
        name='api_public_loan_list_detail'
    ),

    # private
    path(
        f'{VERSION}/private/list',
        ApiPrivateLoanViewSet.as_view(URL_READ_ONLY),
        name='api_private_loan_list_detail'
    ),
    path(
        f'{VERSION}/private/create',
        ApiPrivateLoanViewSet.as_view(URL_CREATE),
        name='api_private_loan_create'
    ),
    path(
        f'{VERSION}/private/<pk>/update',
        ApiPrivateLoanViewSet.as_view(URL_UPDATE),
        name='api_private_loan_update'
    ),
    path(
        f'{VERSION}/private/<pk>/delete',
        ApiPrivateLoanViewSet.as_view(URL_DELETE),
        name='api_private_loan_delete'
    ),
]

"""
Add to urls.py urlpatterns:
    path('loan/api/', include('loans.controllers.restapi.loan.urls'))
