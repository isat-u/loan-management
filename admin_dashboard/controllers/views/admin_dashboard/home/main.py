"""
CAPSU Accreditation Project
Description for CAPSU Accreditation Project

Author: Mark Jun Gersaniva (markjungersaniva@gmail.com)
Version: 0.0.1
"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View

from accounts.mixins.user_type_mixins import IsAdminViewMixin
from accounts.models import Account
from accounts.models.account.constants import SUPERADMIN, ADMIN, USER
from loans.models.loan.models import Loan
from loans.models.loan_type.models import LoanType
from payments.models.payment_request.models import PaymentRequest


class AdminDashboardHomeView(LoginRequiredMixin, IsAdminViewMixin, View):
    """
    Admin Dashboard Home.

    Allowed HTTP verbs:
        - GET

    Restrictions:
        - LoginRequired
        - Admin user

    """

    def get(self, request, *args, **kwargs):
        users = Account.objects.all()
        loans = Loan.objects.all()
        loan_types = LoanType.objects.all()
        loan_summary = []
        payment_requests = PaymentRequest.objects.filter(status='pending')
        pending_loans = loans.filter(is_active=False)

        for loan_type in loan_types:
            data = {'loan_type': loan_type, 'count': loans.filter(type=loan_type).count()}
            loan_summary.append(data)

        context = {
            "page_title": f"Admin Dashboards",
            "menu_section": "admin_dashboard",
            "menu_subsection": "admin_dashboard",
            "menu_action": "home",
            "users": users,
            "loans": loans,
            "loan_summary": loan_summary,
            "payment_requests": payment_requests,
            "pending_loans": pending_loans,
        }

        return render(request, "admin_dashboard/home/home.html", context)
