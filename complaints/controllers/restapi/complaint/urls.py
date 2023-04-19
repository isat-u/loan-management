from django.urls import path
from loan_management.urls import (
    URL_READ_ONLY,
    URL_DETAIL,
    URL_CREATE,
    URL_UPDATE,
    URL_DELETE
)

from .api import(
    ApiPublicComplaintListDetail,
    ApiPrivateComplaintViewSet
)

VERSION = 'v1'

urlpatterns = [
    # public
    path(
        f'{VERSION}/public/list',
        ApiPublicComplaintListDetail.as_view(URL_READ_ONLY),
        name='api_public_complaint_list_detail'
    ),

    # private
    path(
        f'{VERSION}/private/list',
        ApiPrivateComplaintViewSet.as_view(URL_READ_ONLY),
        name='api_private_complaint_list_detail'
    ),
    path(
        f'{VERSION}/private/create',
        ApiPrivateComplaintViewSet.as_view(URL_CREATE),
        name='api_private_complaint_create'
    ),
    path(
        f'{VERSION}/private/<pk>/update',
        ApiPrivateComplaintViewSet.as_view(URL_UPDATE),
        name='api_private_complaint_update'
    ),
    path(
        f'{VERSION}/private/<pk>/delete',
        ApiPrivateComplaintViewSet.as_view(URL_DELETE),
        name='api_private_complaint_delete'
    ),
]

"""
Add to urls.py urlpatterns:
    path('complaint/api/', include('complaints.controllers.restapi.complaint.urls'))
