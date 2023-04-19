"""
CAPSU Accreditation Project
Description for CAPSU Accreditation Project

Author: Mark Jun Gersaniva (markjungersaniva@gmail.com)
Version: 0.0.1
"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View

from accounts.mixins.user_type_mixins import IsUserViewMixin
from accounts.models import Account
from accounts.models.account.constants import SUPERADMIN, ADMIN, USER


class UserDashboardHomeView(LoginRequiredMixin, IsUserViewMixin, View):
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
            "page_title": f"User Dashboard",
            "menu_section": "user_dashboard",
            "menu_subsection": "user_dashboard",
            "menu_action": "home",
            "users": users,

        }

        return render(request, "user_dashboard/home/home.html", context)
