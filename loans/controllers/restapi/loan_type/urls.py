from django.urls import path
from loan_management.urls import (
    URL_READ_ONLY,
    URL_DETAIL,
    URL_CREATE,
    URL_UPDATE,
    URL_DELETE
)

from .api import(
    ApiPublicLoanTypeListDetail,
    ApiPrivateLoanTypeViewSet
)

VERSION = 'v1'

urlpatterns = [
    # public
    path(
        f'{VERSION}/public/list',
        ApiPublicLoanTypeListDetail.as_view(URL_READ_ONLY),
        name='api_public_loan_type_list_detail'
    ),

    # private
    path(
        f'{VERSION}/private/list',
        ApiPrivateLoanTypeViewSet.as_view(URL_READ_ONLY),
        name='api_private_loan_type_list_detail'
    ),
    path(
        f'{VERSION}/private/create',
        ApiPrivateLoanTypeViewSet.as_view(URL_CREATE),
        name='api_private_loan_type_create'
    ),
    path(
        f'{VERSION}/private/<pk>/update',
        ApiPrivateLoanTypeViewSet.as_view(URL_UPDATE),
        name='api_private_loan_type_update'
    ),
    path(
        f'{VERSION}/private/<pk>/delete',
        ApiPrivateLoanTypeViewSet.as_view(URL_DELETE),
        name='api_private_loan_type_delete'
    ),
]

