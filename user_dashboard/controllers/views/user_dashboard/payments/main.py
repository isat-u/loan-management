"""
Loan Management
Description for Loan Management

Author: Maayon (maayon@gmail.com)
Version: 0.0.1
"""
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import View
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.models import ST_PP_COMPLETED
from django.dispatch import receiver
from paypal.standard.ipn.signals import valid_ipn_received
from paypal.standard.forms import PayPalPaymentsForm

from accounts.mixins.user_type_mixins import IsUserViewMixin
from accounts.models import Account
from loans.models import Loan
from payments.controllers.restapi.payment_history.serializers import PaypalIPNCustomSerializer
from payments.models import PaymentHistory, PaymentHistoryError

from payments.models.payment_request import PaymentRequest as Master
from user_dashboard.controllers.views.user_dashboard.payments.forms import PaymentRequestForm as MasterForm

"""
URLS
# Payment

from user_dashboard.controllers.views.user_dashboard.payments import main as payments_views

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
        'payment/create',
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
"""


class UserDashboardPaymentRequestListView(LoginRequiredMixin, IsUserViewMixin, View):
    """ 
    List view for Payments. 
    
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
        obj_list = Master.objects.actives()
        paginator = Paginator(obj_list, 50)
        page = request.GET.get('page')
        objs = paginator.get_page(page)

        context = {
            "page_title": f"Payments",
            "menu_section": "user_dashboard",
            "menu_subsection": "payment",
            "menu_action": "list",
            "paginator": paginator,
            "objects": objs
        }

        return render(request, "user_dashboard/payments/list.html", context)


class UserDashboardPaymentRequestCreateView(LoginRequiredMixin, IsUserViewMixin, View):
    """ 
    Create view for Payments. 
    
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
        account_pk = kwargs.get('account', None)
        loan_pk = kwargs.get('loan', None)

        if account_pk and loan_pk:
            account = Account.objects.get(pk=account_pk)
            loan = Loan.objects.get(pk=loan_pk)
            form = MasterForm(initial={'account': account, 'loan': loan})
        else:
            form = MasterForm

        context = {
            "page_title": "Create new Payment",
            "menu_section": "user_dashboard",
            "menu_subsection": "payment",
            "menu_action": "create",
            "form": form
        }

        return render(request, "user_dashboard/payments/form.html", context)

    def post(self, request, *args, **kwargs):
        form = MasterForm(data=request.POST)
        next = request.POST.get('next', '/')

        if form.is_valid():
            data = form.save(commit=False)
            data.created_by = request.user

            # check payment_source
            if data.payment_source == 'paypal':
                payment_history = PaymentHistory.objects.create(
                    payment_source=data.payment_source,
                    amount=data.amount,
                    loan=data.loan,
                    currency='PHP',
                    account=request.user,
                )
                invoice = PaymentHistory.objects.get(invoice_number=request.GET.get('invoice'))
                data.invoice = invoice
                data.save()

                return_url = request.build_absolute_uri(reverse('payment_paypal_success_view'))
                if '?' in return_url:
                    return_url = return_url + '&invoice=' + payment_history.invoice_number
                else:
                    return_url = return_url + '?invoice=' + payment_history.invoice_number

                cancel_url = request.build_absolute_uri(reverse('payment_paypal_cancelled_view'))
                if '?' in cancel_url:
                    cancel_url = cancel_url + '&invoice=' + payment_history.invoice_number
                else:
                    cancel_url = cancel_url + '?invoice=' + payment_history.invoice_number

                paypal_dict = {
                    "business": settings.PAYPAL_RECEIVER_EMAIL,
                    "amount": data.amount,
                    "item_name": 'Loan Payment',
                    "invoice": payment_history.invoice_number,
                    "currency_code": "PHP",
                    "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
                    "return": return_url,
                    "cancel_return": cancel_url,
                    "custom": request.user.email,  # Custom command to correlate to some function later (optional)
                }

                paypal_form = PayPalPaymentsForm(initial=paypal_dict, button_type="donate")
                context = {
                    'page_title': 'Loan Management',
                    'amount': data.amount,
                    'invoice': payment_history.invoice_number,
                    'payment_source': data.payment_source,
                    'paypal_form': paypal_form,
                }

                if data.payment_source == 'paypal':
                    return render(request, 'user_dashboard/paypal/process.html', context)
                return HttpResponseRedirect(next)
        else:
            context = {
                "page_title": "Create new Payment",
                "menu_section": "user_dashboard",
                "menu_subsection": "payment",
                "menu_action": "create",
                "form": form
            }

            messages.error(
                request,
                'There were errors processing your request:',
                extra_tags='danger'
            )
            return render(request, "user_dashboard/payments/form.html", context)


class UserDashboardPaymentRequestDetailView(LoginRequiredMixin, IsUserViewMixin, View):
    """ 
    Create view for Payments. 
    
    Allowed HTTP verbs: 
        - GET
    
    Restrictions:
        - LoginRequired
        - User user

    Filters:
        - pk = kwargs.get('pk')
    """

    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(Master, pk=kwargs.get('payment', None))
        context = {
            "page_title": f"Payment: {obj}",
            "menu_section": "user_dashboard",
            "menu_subsection": "payment",
            "menu_action": "detail",
            "obj": obj
        }

        return render(request, "user_dashboard/payments/detail.html", context)


class UserDashboardPaymentRequestUpdateView(LoginRequiredMixin, IsUserViewMixin, View):
    """ 
    Create view for Payments. 
    
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
        obj = get_object_or_404(Master, pk=kwargs.get('payment', None))
        form = MasterForm(instance=obj)

        context = {
            "page_title": f"Update Payment: {obj}",
            "menu_section": "user_dashboard",
            "menu_subsection": "payment",
            "menu_action": "update",
            "obj": obj,
            "form": form
        }

        return render(request, "user_dashboard/payments/form.html", context)

    def post(self, request, *args, **kwargs):
        obj = get_object_or_404(Master, pk=kwargs.get('payment', None))
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
                    'user_dashboard_payments_detail',
                    kwargs={
                        'payment': data.pk
                    }
                )
            )
        else:
            context = {
                "page_title": "Update Payment: {obj}",
                "menu_section": "user_dashboard",
                "menu_subsection": "payment",
                "menu_action": "update",
                "obj": obj,
                "form": form
            }

            messages.error(
                request,
                'There were errors processing your request:',
                extra_tags='danger'
            )
            return render(request, "user_dashboard/payments/form.html", context)


class UserDashboardPaymentRequestDeleteView(LoginRequiredMixin, IsUserViewMixin, View):
    """ 
    Create view for Payments. 
    
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
        obj = get_object_or_404(Master, pk=kwargs.get('payment', None))
        context = {
            "page_title": f"Delete Payment: {obj}",
            "menu_section": "user_dashboard",
            "menu_subsection": "payment",
            "menu_action": "delete",
            "obj": obj
        }

        return render(request, "user_dashboard/payments/delete.html", context)

    def post(self, request, *args, **kwargs):
        obj = get_object_or_404(Master, pk=kwargs.get('payment', None))

        messages.success(
            request,
            f'{obj} deleted!',
            extra_tags='success'
        )

        obj.delete()

        return HttpResponseRedirect(
            reverse(
                'user_dashboard_payments_list'
            )
        )

# PayPal
@csrf_exempt
def payment_done(request):
    if request.user.is_authenticated:
        user = request.user

        if not 'invoice' in request.GET:
            return payment_cancelled()

        try:
            payment_history = PaymentHistory.objects.get(invoice_number=request.GET.get('invoice'))
        except PaymentHistory.DoesNotExist:
            return payment_cancelled()

        payment_history.status = 'COMPLETED'
        payment_history.save()

        try:
            payment_request = Master.objects.get(account=user)
            payment_request.status = 'completed'
            payment_request.save()

            context = {
                'page_title': 'Thank you',
                'user': user,
            }
            return render(request, 'payment/paypal/success.html', context)
        except Master.DoesNotExist:
            return HttpResponseRedirect(reverse('page_404'))
    return HttpResponseRedirect(reverse('home_login_view'))


def payment_cancelled(request, *args, **kwargs):
    if 'invoice' in request.GET:
        invoice = request.GET.get('invoice')
        print(invoice)
        payment_history = PaymentHistory.objects.get(invoice_number=invoice)
        payment_history.status = 'CANCELLED'
        payment_history.save()

    return render(request, 'payment/paypal/failed.html')


@receiver(valid_ipn_received)
def ipn_receiver(sender, **kwargs):
    # TODO:
    # connect this to PaymentHistory
    ipn_obj = sender
    history = None
    ipn_data = PaypalIPNCustomSerializer(ipn_obj)

    try:
        history = PaymentHistory.objects.get(invoice_number=ipn_obj.invoice)
        history.provider_data = ipn_data.data

    except PaymentHistory.DoesNotExist:
        PaymentHistoryError.objects.create(
            payment_source='paypal',
            reason='Invoice does not exist',
            provider_data=ipn_data.data,
            invoice_number=ipn_obj.invoice
        )

    if ipn_obj.txn_type == 'web_accept':
        if ipn_obj.payment_status == ST_PP_COMPLETED:
            # payment was successful
            user = Account.objects.get(email=ipn_obj.custom)
            user.is_verified = True
            user.save()

    if history:
        history.status = ipn_obj.payment_status
        history.save()
