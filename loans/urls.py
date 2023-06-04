from django.urls import path, include

from .controllers.restapi.loan.api import ApiPrivateLoanViewSet

version = 'api/v1'

READ_ONLY = {
  'get': 'list'
}
urlpatterns = [
    path(f'{version}/loan', ApiPrivateLoanViewSet.as_view(READ_ONLY), name='user_loans'),
    path('loan_type/api/', include('loans.controllers.restapi.loan_type.urls'))
]
