from django.urls import path
from admin_dashboard.controllers.views.admin_dashboard.home import main as home_views
from admin_dashboard.controllers.views.admin_dashboard.accounts import main as accounts_views
from admin_dashboard.controllers.views.admin_dashboard.profiles import main as profiles_views

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
