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

from loans.models.loan_type.models import LoanType as Master
from admin_dashboard.controllers.views.admin_dashboard.loan_types.forms import LoanTypeForm as MasterForm

"""
URLS
# Loan Type

from admin_dashboard.controllers.views.admin_dashboard.loan_types import main as loan_types_views

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
"""


class AdminDashboardLoanTypeListView(LoginRequiredMixin, IsAdminViewMixin, View):
    """ 
    List view for Loan Types. 
    
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
            "page_title": f"Loan Types",
            "menu_section": "admin_dashboard",
            "menu_subsection": "loan_type",
            "menu_action": "list",
            "paginator": paginator,
            "objects": objs
        }

        return render(request, "admin_dashboard/loan_types/list.html", context)


class AdminDashboardLoanTypeCreateView(LoginRequiredMixin, IsAdminViewMixin, View):
    """ 
    Create view for Loan Types. 
    
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
            "page_title": "Create new Loan Type",
            "menu_section": "admin_dashboard",
            "menu_subsection": "loan_type",
            "menu_action": "create",
            "form": form
        }

        return render(request, "admin_dashboard/loan_types/form.html", context)
    
    def post(self, request, *args, **kwargs):
        form = MasterForm(data=request.POST)
        counter = request.POST.get('counter', 0)
        meta = {}

        if counter:
            for count in range(int(counter)):
                meta[request.POST.get(f"years_{count}")] = {
                    "yearly_interest": request.POST.get(f"yearly_{count}", 0),
                    "monthly_interest": request.POST.get(f"monthly_{count}", 0),
               }

        if form.is_valid():
            data = form.save(commit=False)
            data.created_by = request.user
            data.meta = meta
            data.save()
            
            messages.success(
                request,
                f'{data} saved!',
                extra_tags='success'
            )

            return HttpResponseRedirect(
                reverse(
                    'admin_dashboard_loan_types_detail',
                    kwargs={
                        'loan_type': data.pk
                    }
                )
            )
        else:
            context = {
                "page_title": "Create new Loan Type",
                "menu_section": "admin_dashboard",
                "menu_subsection": "loan_type",
                "menu_action": "create",
                "form": form
            }

            messages.error(
                request,
                'There were errors processing your request:',
                extra_tags='danger'
            )
            return render(request, "admin_dashboard/loan_types/form.html", context)


class AdminDashboardLoanTypeDetailView(LoginRequiredMixin, IsAdminViewMixin, View):
    """ 
    Create view for Loan Types. 
    
    Allowed HTTP verbs: 
        - GET
    
    Restrictions:
        - LoginRequired
        - Admin user

    Filters:
        - pk = kwargs.get('pk')
    """

    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(Master, pk=kwargs.get('loan_type', None))
        context = {
            "page_title": f"Loan Type: {obj}",
            "menu_section": "admin_dashboard",
            "menu_subsection": "loan_type",
            "menu_action": "detail",
            "obj": obj
        }

        return render(request, "admin_dashboard/loan_types/detail.html", context)


class AdminDashboardLoanTypeUpdateView(LoginRequiredMixin, IsAdminViewMixin, View):
    """ 
    Create view for Loan Types. 
    
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
        obj = get_object_or_404(Master, pk=kwargs.get('loan_type', None))
        form = MasterForm(instance=obj)

        context = {
            "page_title": f"Update Loan Type: {obj}",
            "menu_section": "admin_dashboard",
            "menu_subsection": "loan_type",
            "menu_action": "update",
            "obj": obj,
            "form": form
        }

        return render(request, "admin_dashboard/loan_types/form.html", context)
    
    def post(self, request, *args, **kwargs):
        obj = get_object_or_404(Master, pk=kwargs.get('loan_type', None))
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
                    'admin_dashboard_loan_types_detail',
                    kwargs={
                        'loan_type': data.pk
                    }
                )
            )
        else:
            context = {
                "page_title": "Update Loan Type: {obj}",
                "menu_section": "admin_dashboard",
                "menu_subsection": "loan_type",
                "menu_action": "update",
                "obj": obj,
                "form": form
            }

            messages.error(
                request,
                'There were errors processing your request:',
                extra_tags='danger'
            )
            return render(request, "admin_dashboard/loan_types/form.html", context)


class AdminDashboardLoanTypeDeleteView(LoginRequiredMixin, IsAdminViewMixin, View):
    """ 
    Create view for Loan Types. 
    
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
        obj = get_object_or_404(Master, pk=kwargs.get('loan_type', None))
        context = {
            "page_title": f"Delete Loan Type: {obj}",
            "menu_section": "admin_dashboard",
            "menu_subsection": "loan_type",
            "menu_action": "delete",
            "obj": obj
        }

        return render(request, "admin_dashboard/loan_types/delete.html", context)
    
    def post(self, request, *args, **kwargs):
        obj = get_object_or_404(Master, pk=kwargs.get('loan_type', None))

        messages.success(
            request,
            f'{obj} deleted!',
            extra_tags='success'
        )

        obj.delete()

        return HttpResponseRedirect(
            reverse(
                'admin_dashboard_loan_types_list'
            )
        )
