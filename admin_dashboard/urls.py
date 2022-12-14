from django.urls import path
from admin_dashboard.controllers.views.admin_dashboard.home import main as home_views
from admin_dashboard.controllers.views.admin_dashboard.accounts import main as accounts_views
from admin_dashboard.controllers.views.admin_dashboard.profiles import main as profiles_views
from admin_dashboard.controllers.views.admin_dashboard.loans import main as loans_views
from admin_dashboard.controllers.views.admin_dashboard.loan_types import main as loan_types_views

urlpatterns = [
    path(
        '',
        home_views.AdminDashboardHomeView.as_view(),
        name='admin_dashboard_home_view'
    ),
]

urlpatterns += [
    path(
        'account/list',
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
        'profile/<profile>/update',
        profiles_views.AdminDashboardProfileUpdateView.as_view(),
        name='admin_dashboard_profiles_update'
    ),
    path(
        'profile/<profile>/delete',
        profiles_views.AdminDashboardProfileDeleteView.as_view(),
        name='admin_dashboard_profiles_delete'
    )
]

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
    )
]

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
