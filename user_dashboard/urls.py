from django.urls import path
from user_dashboard.controllers.views.user_dashboard.home import main as home_views
from user_dashboard.controllers.views.user_dashboard.loans import main as loans_views
from user_dashboard.controllers.views.user_dashboard.payments import main as payments_views

urlpatterns = [
    path(
        '',
        home_views.UserDashboardHomeView.as_view(),
        name='user_dashboard_home_view'
    ),
]

urlpatterns += [
    path(
        'loan/<account>/list',
        loans_views.UserDashboardLoanListView.as_view(),
        name='user_dashboard_loans_list'
    ),
    path(
        'loan/<loan>/detail',
        loans_views.UserDashboardLoanDetailView.as_view(),
        name='user_dashboard_loans_detail'
    ),
    path(
        'loan/create',
        loans_views.UserDashboardLoanCreateView.as_view(),
        name='user_dashboard_loans_create'
    ),
    path(
        'loan/<loan>/update',
        loans_views.UserDashboardLoanUpdateView.as_view(),
        name='user_dashboard_loans_update'
    ),
    path(
        'loan/<loan>/delete',
        loans_views.UserDashboardLoanDeleteView.as_view(),
        name='user_dashboard_loans_delete'
    )
]

urlpatterns += [
    path(
        'payment/list',
        payments_views.UserDashboardPaymentRequestListView.as_view(),
        name='user_dashboard_payments_list'
    ),
    path(
        'payment/<payment>/detail',
        payments_views.UserDashboardPaymentRequestDetailView.as_view(),
        name='user_dashboard_payments_detail'
    ),
    path(
        'payment/<account>/<loan>/create',
        payments_views.UserDashboardPaymentRequestCreateView.as_view(),
        name='user_dashboard_payments_create'
    ),
    path(
        'payment/<payment>/update',
        payments_views.UserDashboardPaymentRequestUpdateView.as_view(),
        name='user_dashboard_payments_update'
    ),
    path(
        'payment/<payment>/delete',
        payments_views.UserDashboardPaymentRequestDeleteView.as_view(),
        name='user_dashboard_payments_delete'
    )
]
