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
from accounts.models import Account
from amortizations.models import Amortization
from loans.models import LoanType
from loans.models.loan.constants import LOAN_INTERESTS

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
        account = Account.objects.get(pk=kwargs.get('account', None))
        form = MasterForm

        if account:
            form = MasterForm(initial={'account': account})

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
            loan_type = form.cleaned_data['type']
            loan_years = form.cleaned_data['years'] if form.cleaned_data['years'] is not None else 1
            loan_details = LOAN_INTERESTS.get(f'{loan_type}')[loan_years]

            data = form.save(commit=False)
            data.yearly_interest = loan_details.get('yearly_interest')
            data.monthly_interest = loan_details.get('monthly_interest')
            data.created_by = request.user
            data.save()

            # generate amortization
            amount = data.amount
            months = data.years * 12
            ideal_principal = data.amount / months
            ideal_balance = amount
            actual_balance = amount
            actual_monthly_amortization = data.monthly_amortization

            for month in range(months):
                month += 1
                ideal_interest = ideal_balance * data.monthly_interest
                ideal_balance = ideal_balance - ideal_principal
                ideal_monthly_amortization = ideal_principal + ideal_interest
                print(
                    f'{month} - {ideal_principal}, {ideal_interest:.2f}, {ideal_monthly_amortization}, {ideal_balance}')

                actual_interest = actual_balance * data.monthly_interest
                actual_principal = actual_monthly_amortization - actual_interest
                actual_balance = actual_balance - actual_principal
                print(
                    f'{month} - {actual_principal}, {actual_interest:.2f}, {actual_monthly_amortization}, {actual_balance}')
                Amortization.objects.create(
                    month=month,
                    ideal_principal=ideal_principal,
                    ideal_interest=ideal_interest,
                    ideal_monthly_amortization=ideal_monthly_amortization,
                    ideal_balance=ideal_balance,
                    actual_principal=actual_principal,
                    actual_interest=actual_interest,
                    actual_monthly_amortization=actual_monthly_amortization,
                    actual_balance=actual_balance,
                    loan=data,
                    created_by=request.user
                )

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
