from django.urls import path

from .controllers.restapi.loan.api import ApiPrivateLoanViewSet

version = 'api/v1'

READ_ONLY = {
  'get': 'list'
}
urlpatterns = [
    path(f'{version}/loan', ApiPrivateLoanViewSet.as_view(READ_ONLY), name='user_loans'),
]