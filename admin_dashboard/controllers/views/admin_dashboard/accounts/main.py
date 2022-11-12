"""
Loan Management
Description for Loan Management

Author: Maayon (maayon@gmail.com)
Version: 0.0.1
"""
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import View
from django.core.paginator import Paginator

from accounts.mixins.user_type_mixins import IsAdminViewMixin

from accounts.models.account.models import Account as Master
from admin_dashboard.controllers.views.admin_dashboard.accounts.forms import AccountForm as MasterForm

"""
URLS
# Account

from admin_dashboard.controllers.views.admin_dashboard.accounts import main as accounts_views

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
"""


class AdminDashboardAccountListView(LoginRequiredMixin, IsAdminViewMixin, View):
    """ 
    List view for Accounts. 
    
    Allowed HTTP verbs: 
        - GET
    
    Restrictions:
        - LoginRequired
        - Admin user

    Filters:
        - Optionally used more multi-user/multi-tenant apps to separate ownership
        - ex: company=kwargs.get('company')
    """

    def get(self, request, *args, **kwargs):
        obj_list = Master.objects.actives()
        paginator = Paginator(obj_list, 50)
        page = request.GET.get('page')
        objs = paginator.get_page(page)

        context = {
            "page_title": f"Accounts",
            "menu_section": "admin_dashboard",
            "menu_subsection": "account",
            "menu_action": "list",
            "paginator": paginator,
            "objects": objs
        }

        return render(request, "admin_dashboard/accounts/list.html", context)


class AdminDashboardAccountCreateView(LoginRequiredMixin, IsAdminViewMixin, View):
    """ 
    Create view for Accounts. 
    
    Allowed HTTP verbs: 
        - GET
        - POST
    
    Restrictions:
        - LoginRequired
        - Admin user

    Filters:
        - Optionally used more multi-user/multi-tenant apps to separate ownership
        - ex: company=kwargs.get('company')
    """

    def get(self, request, *args, **kwargs):
        form = MasterForm
        context = {
            "page_title": "Create new Account",
            "menu_section": "admin_dashboard",
            "menu_subsection": "account",
            "menu_action": "create",
            "form": form
        }

        return render(request, "admin_dashboard/accounts/form.html", context)
    
    def post(self, request, *args, **kwargs):
        form = MasterForm(data=request.POST)

        if form.is_valid():
            data = form.save(commit=False)
            data.created_by = request.user
            data.save()
            messages.success(
                request,
                f'{data} saved!',
                extra_tags='success'
            )

            return HttpResponseRedirect(
                reverse(
                    'admin_dashboard_profiles_update',
                    kwargs={
                        'profile': data.profile.pk
                    }
                )
            )
        else:
            context = {
                "page_title": "Create new Account",
                "menu_section": "admin_dashboard",
                "menu_subsection": "account",
                "menu_action": "create",
                "form": form
            }

            messages.error(
                request,
                'There were errors processing your request:',
                extra_tags='danger'
            )
            return render(request, "admin_dashboard/accounts/form.html", context)


class AdminDashboardAccountDetailView(LoginRequiredMixin, IsAdminViewMixin, View):
    """ 
    Create view for Accounts. 
    
    Allowed HTTP verbs: 
        - GET
    
    Restrictions:
        - LoginRequired
        - Admin user

    Filters:
        - pk = kwargs.get('pk')
    """

    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(Master, pk=kwargs.get('account', None))

        context = {
            "page_title": f"Account: {obj}",
            "menu_section": "admin_dashboard",
            "menu_subsection": "account",
            "menu_action": "detail",
            "obj": obj
        }

        return render(request, "admin_dashboard/accounts/detail.html", context)


class AdminDashboardAccountUpdateView(LoginRequiredMixin, IsAdminViewMixin, View):
    """ 
    Create view for Accounts. 
    
    Allowed HTTP verbs: 
        - GET
        - POST
    
    Restrictions:
        - LoginRequired
        - Admin user

    Filters:
        - pk = kwargs.get('pk')
    """

    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(Master, pk=kwargs.get('account', None))
        form = MasterForm(instance=obj)

        context = {
            "page_title": f"Update Account: {obj}",
            "menu_section": "admin_dashboard",
            "menu_subsection": "account",
            "menu_action": "update",
            "obj": obj,
            "form": form
        }

        return render(request, "admin_dashboard/accounts/form.html", context)
    
    def post(self, request, *args, **kwargs):
        obj = get_object_or_404(Master, pk=kwargs.get('account', None))
        form = MasterForm(instance=obj, data=request.POST)

        if form.is_valid():
            data = form.save(commit=False)
            data.updated_by = request.user
            data = form.save()
            messages.success(
                request,
                f'{data} saved!',
                extra_tags='success'
            )

            return HttpResponseRedirect(
                reverse(
                    'admin_dashboard_accounts_detail',
                    kwargs={
                        'account': data.pk
                    }
                )
            )
        else:
            context = {
                "page_title": "Update Account: {obj}",
                "menu_section": "admin_dashboard",
                "menu_subsection": "account",
                "menu_action": "update",
                "obj": obj,
                "form": form
            }

            messages.error(
                request,
                'There were errors processing your request:',
                extra_tags='danger'
            )
            return render(request, "admin_dashboard/accounts/form.html", context)


class AdminDashboardAccountDeleteView(LoginRequiredMixin, IsAdminViewMixin, View):
    """ 
    Create view for Accounts. 
    
    Allowed HTTP verbs: 
        - GET
        - POST
    
    Restrictions:
        - LoginRequired
        - Admin user

    Filters:
        - pk = kwargs.get('pk')
    """

    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(Master, pk=kwargs.get('account', None))
        context = {
            "page_title": f"Delete Account: {obj}",
            "menu_section": "admin_dashboard",
            "menu_subsection": "account",
            "menu_action": "delete",
            "obj": obj
        }

        return render(request, "admin_dashboard/accounts/delete.html", context)
    
    def post(self, request, *args, **kwargs):
        obj = get_object_or_404(Master, pk=kwargs.get('account', None))

        messages.success(
            request,
            f'{obj} deleted!',
            extra_tags='success'
        )

        obj.delete()

        return HttpResponseRedirect(
            reverse(
                'admin_dashboard_accounts_list'
            )
        )
