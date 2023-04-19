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

from accounts.mixins.user_type_mixins import IsUserViewMixin

from complaints.models.complaint.models import Complaint as Master
from user_dashboard.controllers.views.user_dashboard.complaints.forms import ComplaintForm as MasterForm

"""
URLS
# Complaint

from user_dashboard.controllers.views.user_dashboard.complaints import main as complaints_views

urlpatterns += [
    path(
        'complaint/list',
        complaints_views.UserDashboardComplaintListView.as_view(),
        name='user_dashboard_complaints_list'
    ),
    path(
        'complaint/<complaint>/detail',
        complaints_views.UserDashboardComplaintDetailView.as_view(),
        name='user_dashboard_complaints_detail'
    ),
    path(
        'complaint/create',
        complaints_views.UserDashboardComplaintCreateView.as_view(),
        name='user_dashboard_complaints_create'
    ),
    path(
        'complaint/<complaint>/update',
        complaints_views.UserDashboardComplaintUpdateView.as_view(),
        name='user_dashboard_complaints_update'
    ),
    path(
        'complaint/<complaint>/delete',
        complaints_views.UserDashboardComplaintDeleteView.as_view(),
        name='user_dashboard_complaints_delete'
    )
]
"""


class UserDashboardComplaintListView(LoginRequiredMixin, IsUserViewMixin, View):
    """ 
    List view for Complaints. 
    
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
        account = request.user
        obj_list = Master.objects.actives().filter(created_by=account)
        paginator = Paginator(obj_list, 50)
        page = request.GET.get('page')
        objs = paginator.get_page(page)

        context = {
            "page_title": f"Complaints",
            "menu_section": "user_dashboard",
            "menu_subsection": "complaint",
            "menu_action": "list",
            "paginator": paginator,
            "objects": objs
        }

        return render(request, "user_dashboard/complaints/list.html", context)


class UserDashboardComplaintCreateView(LoginRequiredMixin, IsUserViewMixin, View):
    """ 
    Create view for Complaints. 
    
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
            "page_title": "Create new Complaint",
            "menu_section": "user_dashboard",
            "menu_subsection": "complaint",
            "menu_action": "create",
            "form": form
        }

        return render(request, "user_dashboard/complaints/form.html", context)
    
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
                    'user_dashboard_complaints_detail',
                    kwargs={
                        'complaint': data.pk
                    }
                )
            )
        else:
            context = {
                "page_title": "Create new Complaint",
                "menu_section": "user_dashboard",
                "menu_subsection": "complaint",
                "menu_action": "create",
                "form": form
            }

            messages.error(
                request,
                'There were errors processing your request:',
                extra_tags='danger'
            )
            return render(request, "user_dashboard/complaints/form.html", context)


class UserDashboardComplaintDetailView(LoginRequiredMixin, IsUserViewMixin, View):
    """ 
    Create view for Complaints. 
    
    Allowed HTTP verbs: 
        - GET
    
    Restrictions:
        - LoginRequired
        - User user

    Filters:
        - pk = kwargs.get('pk')
    """

    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(Master, pk=kwargs.get('complaint', None))
        context = {
            "page_title": f"Complaint: {obj}",
            "menu_section": "user_dashboard",
            "menu_subsection": "complaint",
            "menu_action": "detail",
            "obj": obj
        }

        return render(request, "user_dashboard/complaints/detail.html", context)


class UserDashboardComplaintUpdateView(LoginRequiredMixin, IsUserViewMixin, View):
    """ 
    Create view for Complaints. 
    
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
        obj = get_object_or_404(Master, pk=kwargs.get('complaint', None))
        form = MasterForm(instance=obj)

        context = {
            "page_title": f"Update Complaint: {obj}",
            "menu_section": "user_dashboard",
            "menu_subsection": "complaint",
            "menu_action": "update",
            "obj": obj,
            "form": form
        }

        return render(request, "user_dashboard/complaints/form.html", context)
    
    def post(self, request, *args, **kwargs):
        obj = get_object_or_404(Master, pk=kwargs.get('complaint', None))
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
                    'user_dashboard_complaints_detail',
                    kwargs={
                        'complaint': data.pk
                    }
                )
            )
        else:
            context = {
                "page_title": "Update Complaint: {obj}",
                "menu_section": "user_dashboard",
                "menu_subsection": "complaint",
                "menu_action": "update",
                "obj": obj,
                "form": form
            }

            messages.error(
                request,
                'There were errors processing your request:',
                extra_tags='danger'
            )
            return render(request, "user_dashboard/complaints/form.html", context)


class UserDashboardComplaintDeleteView(LoginRequiredMixin, IsUserViewMixin, View):
    """ 
    Create view for Complaints. 
    
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
        obj = get_object_or_404(Master, pk=kwargs.get('complaint', None))
        context = {
            "page_title": f"Delete Complaint: {obj}",
            "menu_section": "user_dashboard",
            "menu_subsection": "complaint",
            "menu_action": "delete",
            "obj": obj
        }

        return render(request, "user_dashboard/complaints/delete.html", context)
    
    def post(self, request, *args, **kwargs):
        obj = get_object_or_404(Master, pk=kwargs.get('complaint', None))

        messages.success(
            request,
            f'{obj} deleted!',
            extra_tags='success'
        )

        obj.delete()

        return HttpResponseRedirect(
            reverse(
                'user_dashboard_complaints_list'
            )
        )
