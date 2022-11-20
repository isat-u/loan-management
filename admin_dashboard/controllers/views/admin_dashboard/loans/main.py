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

from loans.models.loan.models import Loan as Master
from admin_dashboard.controllers.views.admin_dashboard.loans.forms import LoanForm as MasterForm

"""
URLS
# Loan

from admin_dashboard.controllers.views.admin_dashboard.loans import main as loans_views

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
        'loan/create',
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
"""


class AdminDashboardLoanListView(LoginRequiredMixin, IsAdminViewMixin, View):
    """ 
    List view for Loans. 
    
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
            "page_title": f"Loans",
            "menu_section": "admin_dashboard",
            "menu_subsection": "loan",
            "menu_action": "list",
            "paginator": paginator,
            "objects": objs
        }

        return render(request, "admin_dashboard/loans/list.html", context)


class AdminDashboardLoanCreateView(LoginRequiredMixin, IsAdminViewMixin, View):
    """ 
    Create view for Loans. 
    
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
            "page_title": "Create new Loan",
            "menu_section": "admin_dashboard",
            "menu_subsection": "loan",
            "menu_action": "create",
            "form": form
        }

        return render(request, "admin_dashboard/loans/form.html", context)
    
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
                    'admin_dashboard_loans_detail',
                    kwargs={
                        'loan': data.pk
                    }
                )
            )
        else:
            context = {
                "page_title": "Create new Loan",
                "menu_section": "admin_dashboard",
                "menu_subsection": "loan",
                "menu_action": "create",
                "form": form
            }

            messages.error(
                request,
                'There were errors processing your request:',
                extra_tags='danger'
            )
            return render(request, "admin_dashboard/loans/form.html", context)


class AdminDashboardLoanDetailView(LoginRequiredMixin, IsAdminViewMixin, View):
    """ 
    Create view for Loans. 
    
    Allowed HTTP verbs: 
        - GET
    
    Restrictions:
        - LoginRequired
        - Admin user

    Filters:
        - pk = kwargs.get('pk')
    """

    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(Master, pk=kwargs.get('loan', None))
        context = {
            "page_title": f"Loan: {obj}",
            "menu_section": "admin_dashboard",
            "menu_subsection": "loan",
            "menu_action": "detail",
            "obj": obj
        }

        return render(request, "admin_dashboard/loans/detail.html", context)


class AdminDashboardLoanUpdateView(LoginRequiredMixin, IsAdminViewMixin, View):
    """ 
    Create view for Loans. 
    
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
        obj = get_object_or_404(Master, pk=kwargs.get('loan', None))
        form = MasterForm(instance=obj)

        context = {
            "page_title": f"Update Loan: {obj}",
            "menu_section": "admin_dashboard",
            "menu_subsection": "loan",
            "menu_action": "update",
            "obj": obj,
            "form": form
        }

        return render(request, "admin_dashboard/loans/form.html", context)
    
    def post(self, request, *args, **kwargs):
        obj = get_object_or_404(Master, pk=kwargs.get('loan', None))
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
                    'admin_dashboard_loans_detail',
                    kwargs={
                        'loan': data.pk
                    }
                )
            )
        else:
            context = {
                "page_title": "Update Loan: {obj}",
                "menu_section": "admin_dashboard",
                "menu_subsection": "loan",
                "menu_action": "update",
                "obj": obj,
                "form": form
            }

            messages.error(
                request,
                'There were errors processing your request:',
                extra_tags='danger'
            )
            return render(request, "admin_dashboard/loans/form.html", context)


class AdminDashboardLoanDeleteView(LoginRequiredMixin, IsAdminViewMixin, View):
    """ 
    Create view for Loans. 
    
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
        obj = get_object_or_404(Master, pk=kwargs.get('loan', None))
        context = {
            "page_title": f"Delete Loan: {obj}",
            "menu_section": "admin_dashboard",
            "menu_subsection": "loan",
            "menu_action": "delete",
            "obj": obj
        }

        return render(request, "admin_dashboard/loans/delete.html", context)
    
    def post(self, request, *args, **kwargs):
        obj = get_object_or_404(Master, pk=kwargs.get('loan', None))

        messages.success(
            request,
            f'{obj} deleted!',
            extra_tags='success'
        )

        obj.delete()

        return HttpResponseRedirect(
            reverse(
                'admin_dashboard_loans_list'
            )
        )
