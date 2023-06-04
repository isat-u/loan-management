from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from accounts.mixins.user_type_mixins import IsAdminViewMixin
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.core.paginator import Paginator
from payments.models.payment_request.models import PaymentRequest as Master


class AdminDashboardReportListView(LoginRequiredMixin, IsAdminViewMixin, View):
    def get(self, request, *args, **kwargs):
        obj_list = Master.objects.actives().order_by('-created')
        paginator = Paginator(obj_list, 50)
        page = request.GET.get('page')
        objs = paginator.get_page(page)
        print(obj_list)
        context = {
            "page_title": f"Reports",
            "menu_section": "admin_dashboard",
            "menu_subsection": "reports",
            "menu_action": "list",
            "paginator": paginator,
            "objects": objs
        }

        return render(request, "admin_dashboard/reports/list.html", context)