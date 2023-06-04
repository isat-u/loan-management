from django.urls import path
from admin_dashboard.controllers.views.admin_dashboard.home import main as home_views
from admin_dashboard.controllers.views.admin_dashboard.accounts import main as accounts_views
from admin_dashboard.controllers.views.admin_dashboard.profiles import main as profiles_views
from admin_dashboard.controllers.views.admin_dashboard.loans import main as loans_views
from admin_dashboard.controllers.views.admin_dashboard.loan_types import main as loan_types_views
from admin_dashboard.controllers.views.admin_dashboard.payment_requests import main as payment_requests_views
from admin_dashboard.controllers.views.admin_dashboard.reports import main as report_views


urlpatterns = [
    path(
        '',
        home_views.AdminDashboardHomeView.as_view(),
        name='admin_dashboard_home_view'
    ),
]

# Account
urlpatterns += [
    path(
        'account/list/<member_type>',
        accounts_views.AdminDashboardAccountListView.as_view(),
        name='admin_dashboard_accounts_list'
    ),
    path(
        'account/<account>/detail',
        accounts_views.AdminDashboardAccountDetailView.as_view(),
        name='admin_dashboard_accounts_detail'
    ),
    path(
        'account/create',
        accounts_views.AdminDashboardAccountCreateView.as_view(),
        name='admin_dashboard_accounts_create'
    ),
    path(
        'account/<account>/update',
        accounts_views.AdminDashboardAccountUpdateView.as_view(),
        name='admin_dashboard_accounts_update'
    ),
    path(
        'account/<account>/delete',
        accounts_views.AdminDashboardAccountDeleteView.as_view(),
        name='admin_dashboard_accounts_delete'
    )
]

# Profile
urlpatterns += [
    path(
        'profile/list',
        profiles_views.AdminDashboardProfileListView.as_view(),
        name='admin_dashboard_profiles_list'
    ),
    path(
        'profile/<profile>/detail',
        profiles_views.AdminDashboardProfileDetailView.as_view(),
        name='admin_dashboard_profiles_detail'
    ),
    path(
        'profile/create',
        profiles_views.AdminDashboardProfileCreateView.as_view(),
        name='admin_dashboard_profiles_create'
    ),
    path(
        'profile/<profile>/delete',
        profiles_views.AdminDashboardProfileDeleteView.as_view(),
        name='admin_dashboard_profiles_delete'
    ),
    path(
        'profile/<profile>/update',
        profiles_views.DashboardProfileUpdateView.as_view(),
        name='dashboard_profiles_update'
    ),
]

# Loan
urlpatterns += [
    path(
        'loan/list',
        loans_views.AdminDashboardLoanListView.as_view(),
        name='admin_dashboard_loans_list'
    ),
    path(
        'loan/<loan>/detail',
        loans_views.AdminDashboardLoanDetailView.as_view(),
        name='admin_dashboard_loans_detail'
    ),
    path(
        'loan/<account>/create',
        loans_views.AdminDashboardLoanCreateView.as_view(),
        name='admin_dashboard_loans_create'
    ),
    path(
        'loan/<loan>/update',
        loans_views.AdminDashboardLoanUpdateView.as_view(),
        name='admin_dashboard_loans_update'
    ),
    path(
        'loan/<loan>/delete',
        loans_views.AdminDashboardLoanDeleteView.as_view(),
        name='admin_dashboard_loans_delete'
    ),
    path(
        'loan/<loan>/approve',
        loans_views.AdminDashboardLoanApproveView.as_view(),
        name='admin_dashboard_loans_approve'
    )
]

# Loan Type
urlpatterns += [
    path(
        'loan_type/list',
        loan_types_views.AdminDashboardLoanTypeListView.as_view(),
        name='admin_dashboard_loan_types_list'
    ),
    path(
        'loan_type/<loan_type>/detail',
        loan_types_views.AdminDashboardLoanTypeDetailView.as_view(),
        name='admin_dashboard_loan_types_detail'
    ),
    path(
        'loan_type/create',
        loan_types_views.AdminDashboardLoanTypeCreateView.as_view(),
        name='admin_dashboard_loan_types_create'
    ),
    path(
        'loan_type/<loan_type>/update',
        loan_types_views.AdminDashboardLoanTypeUpdateView.as_view(),
        name='admin_dashboard_loan_types_update'
    ),
    path(
        'loan_type/<loan_type>/delete',
        loan_types_views.AdminDashboardLoanTypeDeleteView.as_view(),
        name='admin_dashboard_loan_types_delete'
    )
]

# Payment Request
urlpatterns += [
    path(
        'payment_request/list',
        payment_requests_views.AdminDashboardPaymentRequestListView.as_view(),
        name='admin_dashboard_payment_requests_list'
    ),
    path(
        'payment_request/<payment_request>/detail',
        payment_requests_views.AdminDashboardPaymentRequestDetailView.as_view(),
        name='admin_dashboard_payment_requests_detail'
    ),
    path(
        'payment_request/<account>/<loan>/create',
        payment_requests_views.AdminDashboardPaymentRequestCreateView.as_view(),
        name='admin_dashboard_payment_requests_create'
    ),
    path(
        'payment_request/<payment_request>/update',
        payment_requests_views.AdminDashboardPaymentRequestUpdateView.as_view(),
        name='admin_dashboard_payment_requests_update'
    ),
    path(
        'payment_request/<payment_request>/delete',
        payment_requests_views.AdminDashboardPaymentRequestDeleteView.as_view(),
        name='admin_dashboard_payment_requests_delete'
    ),
    path(
        'payment_request/<payment_request>/complete',
        payment_requests_views.AdminDashboardPaymentRequestCompleteView.as_view(),
        name='admin_dashboard_payment_requests_complete'
    ),
]

# Reports
urlpatterns += [
    path(
        'reports/list',
        report_views.AdminDashboardReportListView.as_view(),
        name='admin_dashboard_reports_view'
    )
]