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

        context = {
            "page_title": f"Admin Dashboards",
            "menu_section": "admin_dashboard",
            "menu_subsection": "admin_dashboard",
            "menu_action": "home",
            "users": users,

        }

        return render(request, "admin_dashboard/home/home.html", context)
