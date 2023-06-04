"""
Loan Management
Description for Loan Management

Author: Maayon (maayon@gmail.com)
Version: 0.0.1
"""
import datetime
import decimal
import math
from dateutil.relativedelta import relativedelta
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import View
from django.core.paginator import Paginator

from accounts.mixins.user_type_mixins import IsUserViewMixin
from accounts.models.account.models import Account
from amortizations.models import Amortization

from loans.models.loan.models import Loan as Master
from loans.models.loan_type.models import LoanType
from user_dashboard.controllers.views.user_dashboard.loans.forms import LoanForm as MasterForm

"""
URLS
# Loan

from user_dashboard.controllers.views.user_dashboard.loans import main as loans_views

urlpatterns += [
    path(
        'loan/list',
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
"""


class UserDashboardLoanListView(LoginRequiredMixin, IsUserViewMixin, View):
    """ 
    List view for Loans. 
    
    Allowed HTTP verbs: 
        - GET
    
    Restrictions:
        - LoginRequired
        - User user

    Filters:
        - Optionally used more multi-user/multi-tenant apps to separate ownership
        - ex: company=kwargs.get('company')
    """

    def get(self, request, *args, **kwargs):
        print(kwargs.get('account', None))
        obj_list = Master.objects.filter(account__pk=kwargs.get('account', None))
        paginator = Paginator(obj_list, 50)
        page = request.GET.get('page')
        objs = paginator.get_page(page)

        context = {
            "page_title": f"Loans",
            "menu_section": "user_dashboard",
            "menu_subsection": "loan",
            "menu_action": "list",
            "paginator": paginator,
            "objects": objs,
        }

        return render(request, "user_dashboard/loans/list.html", context)


class UserDashboardLoanCreateView(LoginRequiredMixin, IsUserViewMixin, View):
    """ 
    Create view for Loans. 
    
    Allowed HTTP verbs: 
        - GET
        - POST
    
    Restrictions:
        - LoginRequired
        - User user

    Filters:
        - Optionally used more multi-user/multi-tenant apps to separate ownership
        - ex: company=kwargs.get('company')
    """

    def get(self, request, *args, **kwargs):
        form = MasterForm
        context = {
            "page_title": "Create new Loan",
            "menu_section": "user_dashboard",
            "menu_subsection": "loan",
            "menu_action": "create",
            "form": form
        }

        return render(request, "user_dashboard/loans/form.html", context)
    
    def post(self, request, *args, **kwargs):
        form = MasterForm(data=request.POST)
        context = {
            "page_title": "Create new Loan",
            "menu_section": "admin_dashboard",
            "menu_subsection": "loan",
            "menu_action": "create",
            "form": form
        }

        if form.is_valid():
            data = form.save(commit=False)
            loan_type = form.cleaned_data['type']
            loan_type = LoanType.objects.get(pk=loan_type.pk)
            loan_months = form.cleaned_data['months'] if form.cleaned_data['months'] is not None else 1

            try:
                maximum_amount = loan_type.meta.get(f'{loan_months}')['maximum_amount']
            except:
                messages.error(
                    request,
                    f'No loan type details for {loan_months} months transaction.',
                    extra_tags='danger'
                )
                return render(request, "user_dashboard/loans/form.html", context)

            if  decimal.Decimal(form.cleaned_data['amount']) > decimal.Decimal(maximum_amount):
                messages.error(
                    request,
                    f'The amount exceeds the maximum loan amount of {maximum_amount}',
                    extra_tags='danger'
                )
                return render(request, "user_dashboard/loans/form.html", context)

            data.account = request.user

            fee = loan_type.meta.get(f'{loan_months}')['fee']
            print('*********')
            print(fee)
            print((decimal.Decimal(fee) / 100))
            data.amount += decimal.Decimal(data.amount) * (decimal.Decimal(fee) / 100)
            print(data.amount)
            if(data.account.is_member):
                data.yearly_interest = loan_type.meta.get(f'{loan_months}')['yearly_reg']
                data.monthly_interest = loan_type.meta.get(f'{loan_months}')['monthly_reg']
            else:
                data.yearly_interest = loan_type.meta.get(f'{loan_months}')['yearly_aso']
                data.monthly_interest = loan_type.meta.get(f'{loan_months}')['monthly_aso']

            months = loan_months
            data.due_date = datetime.date.today() + relativedelta(months=months)
            
            monthly_amortization_percentage = round((decimal.Decimal(data.yearly_interest) / 12) / 100, 2)
            data.maturity = round(data.amount * decimal.Decimal(0.05), 2)
            data.monthly_amortization = round(data.amount * monthly_amortization_percentage, 2)
            
            data.is_active = False
            data.created_by = request.user
            data.save()

            # generate amortization
            amount = decimal.Decimal(data.amount)
            months = data.months
            monthly_interest = decimal.Decimal(data.monthly_interest)
            ideal_principal = amount / months
            ideal_balance = amount
            actual_balance = amount
            actual_monthly_amortization = data.monthly_amortization

            for month in range(months):
                month += 1
                ideal_interest = ideal_balance * (monthly_interest / 100)
                ideal_balance = ideal_balance - ideal_principal
                ideal_monthly_amortization = ideal_principal + ideal_interest

                actual_interest = actual_balance * (monthly_interest / 100)
                actual_principal = actual_monthly_amortization - actual_interest
                actual_balance = actual_balance - actual_principal

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
                    'user_dashboard_loans_detail',
                    kwargs={
                        'loan': data.pk
                    }
                )
            )
        else:
            context = {
                "page_title": "Create new Loan",
                "menu_section": "user_dashboard",
                "menu_subsection": "loan",
                "menu_action": "create",
                "form": form
            }

            messages.error(
                request,
                'There were errors processing your request:',
                extra_tags='danger'
            )
            return render(request, "user_dashboard/loans/form.html", context)


class UserDashboardLoanDetailView(LoginRequiredMixin, IsUserViewMixin, View):
    """ 
    Create view for Loans. 
    
    Allowed HTTP verbs: 
        - GET
    
    Restrictions:
        - LoginRequired
        - User user

    Filters:
        - pk = kwargs.get('pk')
    """

    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(Master, pk=kwargs.get('loan', None))
        completed_payment = obj.payment_requests_loan.filter(status='completed').aggregate(Sum('amount'))
        obj.monthly_interest /= 100
        obj.yearly_interest /= 100
        total_payment = completed_payment['amount__sum']
        if total_payment:
            balance = obj.amount - total_payment
        else:
            balance = obj.amount

        context = {
            "page_title": f"Loan: {obj}",
            "menu_section": "user_dashboard",
            "menu_subsection": "loan",
            "menu_action": "detail",
            "obj": obj,
            "total_payment": total_payment,
            "balance": balance,
        }

        return render(request, "user_dashboard/loans/detail.html", context)


class UserDashboardLoanUpdateView(LoginRequiredMixin, IsUserViewMixin, View):
    """ 
    Create view for Loans. 
    
    Allowed HTTP verbs: 
        - GET
        - POST
    
    Restrictions:
        - LoginRequired
        - User user

    Filters:
        - pk = kwargs.get('pk')
    """

    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(Master, pk=kwargs.get('loan', None))
        form = MasterForm(instance=obj)

        context = {
            "page_title": f"Update Loan: {obj}",
            "menu_section": "user_dashboard",
            "menu_subsection": "loan",
            "menu_action": "update",
            "obj": obj,
            "form": form
        }

        return render(request, "user_dashboard/loans/form.html", context)
    
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
                    'user_dashboard_loans_detail',
                    kwargs={
                        'loan': data.pk
                    }
                )
            )
        else:
            context = {
                "page_title": "Update Loan: {obj}",
                "menu_section": "user_dashboard",
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
            return render(request, "user_dashboard/loans/form.html", context)


class UserDashboardLoanDeleteView(LoginRequiredMixin, IsUserViewMixin, View):
    """ 
    Create view for Loans. 
    
    Allowed HTTP verbs: 
        - GET
        - POST
    
    Restrictions:
        - LoginRequired
        - User user

    Filters:
        - pk = kwargs.get('pk')
    """

    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(Master, pk=kwargs.get('loan', None))
        context = {
            "page_title": f"Delete Loan: {obj}",
            "menu_section": "user_dashboard",
            "menu_subsection": "loan",
            "menu_action": "delete",
            "obj": obj
        }

        return render(request, "user_dashboard/loans/delete.html", context)
    
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
                'user_dashboard_loans_list'
            )
        )
