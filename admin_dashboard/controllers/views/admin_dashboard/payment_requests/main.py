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
from accounts.models.account.models import Account
from loans.models.loan.models import Loan

from payments.models.payment_request.models import PaymentRequest as Master, PaymentRequest
from admin_dashboard.controllers.views.admin_dashboard.payment_requests.forms import PaymentRequestForm as MasterForm

"""
URLS
# Payment Request

from admin_dashboard.controllers.views.admin_dashboard.payment_requests import main as payment_requests_views

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
        'payment_request/create',
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
    )
]
"""


class AdminDashboardPaymentRequestListView(LoginRequiredMixin, IsAdminViewMixin, View):
    """ 
    List view for Payment Requests. 
    
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
            "page_title": f"Payment Requests",
            "menu_section": "admin_dashboard",
            "menu_subsection": "payment_request",
            "menu_action": "list",
            "paginator": paginator,
            "objects": objs
        }

        return render(request, "admin_dashboard/payment_requests/list.html", context)


class AdminDashboardPaymentRequestCreateView(LoginRequiredMixin, IsAdminViewMixin, View):
    """ 
    Create view for Payment Requests. 
    
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
        account_pk = kwargs.get('account', None)
        loan_pk = kwargs.get('loan', None)

        if account_pk and loan_pk:
            account = Account.objects.get(pk=account_pk)
            loan = Loan.objects.get(pk=loan_pk)
            form = MasterForm(initial={'account': account, 'loan': loan})
        else:
            form = MasterForm

        context = {
            "page_title": "Create new Payment Request",
            "menu_section": "admin_dashboard",
            "menu_subsection": "payment_request",
            "menu_action": "create",
            "form": form
        }

        return render(request, "admin_dashboard/payment_requests/form.html", context)
    
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
                    'admin_dashboard_payment_requests_detail',
                    kwargs={
                        'payment_request': data.pk
                    }
                )
            )
        else:
            context = {
                "page_title": "Create new Payment Request",
                "menu_section": "admin_dashboard",
                "menu_subsection": "payment_request",
                "menu_action": "create",
                "form": form
            }

            messages.error(
                request,
                'There were errors processing your request:',
                extra_tags='danger'
            )
            return render(request, "admin_dashboard/payment_requests/form.html", context)


class AdminDashboardPaymentRequestDetailView(LoginRequiredMixin, IsAdminViewMixin, View):
    """ 
    Create view for Payment Requests. 
    
    Allowed HTTP verbs: 
        - GET
    
    Restrictions:
        - LoginRequired
        - Admin user

    Filters:
        - pk = kwargs.get('pk')
    """

    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(Master, pk=kwargs.get('payment_request', None))
        context = {
            "page_title": f"Payment Request: {obj}",
            "menu_section": "admin_dashboard",
            "menu_subsection": "payment_request",
            "menu_action": "detail",
            "obj": obj
        }

        return render(request, "admin_dashboard/payment_requests/detail.html", context)


class AdminDashboardPaymentRequestUpdateView(LoginRequiredMixin, IsAdminViewMixin, View):
    """ 
    Create view for Payment Requests. 
    
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
        obj = get_object_or_404(Master, pk=kwargs.get('payment_request', None))
        form = MasterForm(instance=obj)

        context = {
            "page_title": f"Update Payment Request: {obj}",
            "menu_section": "admin_dashboard",
            "menu_subsection": "payment_request",
            "menu_action": "update",
            "obj": obj,
            "form": form
        }

        return render(request, "admin_dashboard/payment_requests/form.html", context)
    
    def post(self, request, *args, **kwargs):
        obj = get_object_or_404(Master, pk=kwargs.get('payment_request', None))
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
                    'admin_dashboard_payment_requests_detail',
                    kwargs={
                        'payment_request': data.pk
                    }
                )
            )
        else:
            context = {
                "page_title": "Update Payment Request: {obj}",
                "menu_section": "admin_dashboard",
                "menu_subsection": "payment_request",
                "menu_action": "update",
                "obj": obj,
                "form": form
            }

            messages.error(
                request,
                'There were errors processing your request:',
                extra_tags='danger'
            )
            return render(request, "admin_dashboard/payment_requests/form.html", context)


class AdminDashboardPaymentRequestDeleteView(LoginRequiredMixin, IsAdminViewMixin, View):
    """ 
    Create view for Payment Requests. 
    
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
        obj = get_object_or_404(Master, pk=kwargs.get('payment_request', None))
        context = {
            "page_title": f"Delete Payment Request: {obj}",
            "menu_section": "admin_dashboard",
            "menu_subsection": "payment_request",
            "menu_action": "delete",
            "obj": obj
        }

        return render(request, "admin_dashboard/payment_requests/delete.html", context)
    
    def post(self, request, *args, **kwargs):
        obj = get_object_or_404(Master, pk=kwargs.get('payment_request', None))

        messages.success(
            request,
            f'{obj} deleted!',
            extra_tags='success'
        )

        obj.delete()

        return HttpResponseRedirect(
            reverse(
                'admin_dashboard_payment_requests_list'
            )
        )


class AdminDashboardPaymentRequestCompleteView(LoginRequiredMixin, IsAdminViewMixin, View):
    """
    Create view for Payment Requests.

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
        obj = get_object_or_404(Master, pk=kwargs.get('payment_request', None))
        form = MasterForm(instance=obj)

        context = {
            "page_title": f"Complete Payment Request: {obj}",
            "menu_section": "admin_dashboard",
            "menu_subsection": "payment_request",
            "menu_action": "update",
            "obj": obj,
            "form": form
        }

        return render(request, "admin_dashboard/payment_requests/complete.html", context)

    def post(self, request, *args, **kwargs):
        obj = get_object_or_404(Master, pk=kwargs.get('payment_request', None))

        obj.updated_by = request.user
        obj.status = 'completed'
        obj.save()
        messages.success(
            request,
            f'{obj} saved!',
            extra_tags='success'
        )

        return HttpResponseRedirect(
            reverse(
                'admin_dashboard_payment_requests_detail',
                kwargs={
                    'payment_request': obj.pk
                }
            )
        )
