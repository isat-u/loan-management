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

from profiles.models.profile_models import Profile as Master
from admin_dashboard.controllers.views.admin_dashboard.profiles.forms import ProfileForm as MasterForm

"""
URLS
# Profile

from admin_dashboard.controllers.views.admin_dashboard.profiles import main as profiles_views

urlpatterns += [
    path(
        'profile/list',
        profiles_views.AdminDashboardProfileListView.as_view(),
        name='admin_dashboard_profiles_list'
    ),
    path(
        'profile/<profile>/detail',
        profiles_views.AdminDashboardProfileDetailView.as_view(),
        name='admin_dashboard_profiles_detail'
    ),
    path(
        'profile/create',
        profiles_views.AdminDashboardProfileCreateView.as_view(),
        name='admin_dashboard_profiles_create'
    ),
    path(
        'profile/<profile>/update',
        profiles_views.AdminDashboardProfileUpdateView.as_view(),
        name='admin_dashboard_profiles_update'
    ),
    path(
        'profile/<profile>/delete',
        profiles_views.AdminDashboardProfileDeleteView.as_view(),
        name='admin_dashboard_profiles_delete'
    )
]
"""


class AdminDashboardProfileListView(LoginRequiredMixin, IsAdminViewMixin, View):
    """ 
    List view for Profiles. 
    
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
            "page_title": f"Profiles",
            "menu_section": "admin_dashboard",
            "menu_subsection": "profile",
            "menu_action": "list",
            "paginator": paginator,
            "objects": objs
        }

        return render(request, "profiles/list.html", context)


class AdminDashboardProfileCreateView(LoginRequiredMixin, IsAdminViewMixin, View):
    """ 
    Create view for Profiles. 
    
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
            "page_title": "Create new Profile",
            "menu_section": "admin_dashboard",
            "menu_subsection": "profile",
            "menu_action": "create",
            "form": form,
        }

        return render(request, "admin_dashboard/profiles/form.html", context)
    
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
                    'admin_dashboard_loans_create',
                    kwargs={
                        'account': data.account.pk
                    }
                )
            )
        else:
            context = {
                "page_title": "Create new Profile",
                "menu_section": "admin_dashboard",
                "menu_subsection": "profile",
                "menu_action": "create",
                "form": form
            }

            messages.error(
                request,
                'There were errors processing your request:',
                extra_tags='danger'
            )
            return render(request, "admin_dashboard/profiles/form.html", context)


class AdminDashboardProfileDetailView(LoginRequiredMixin, IsAdminViewMixin, View):
    """ 
    Create view for Profiles. 
    
    Allowed HTTP verbs: 
        - GET
    
    Restrictions:
        - LoginRequired
        - Admin user

    Filters:
        - pk = kwargs.get('pk')
    """

    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(Master, pk=kwargs.get('profile', None))
        context = {
            "page_title": f"Profile: {obj}",
            "menu_section": "admin_dashboard",
            "menu_subsection": "profile",
            "menu_action": "detail",
            "obj": obj
        }

        return render(request, "admin_dashboard/accounts/detail.html", context)


class AdminDashboardProfileUpdateView(LoginRequiredMixin, IsAdminViewMixin, View):
    """ 
    Create view for Profiles. 
    
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
        obj = get_object_or_404(Master, pk=kwargs.get('profile', None))
        form = MasterForm(instance=obj)

        context = {
            "page_title": f"Update Profile: {obj}",
            "menu_section": "admin_dashboard",
            "menu_subsection": "profile",
            "menu_action": "update",
            "obj": obj,
            "form": form
        }

        return render(request, "admin_dashboard/profiles/form.html", context)
    
    def post(self, request, *args, **kwargs):
        obj = get_object_or_404(Master, pk=kwargs.get('profile', None))
        form = MasterForm(instance=obj, data=request.POST)
        print('posting *********************')
        if form.is_valid():
            data = form.save(commit=False)
            data.updated_by = request.user
            data = form.save()
            messages.success(
                request,
                f'{data} saved!',
                extra_tags='success'
            )
            print('data.account.pk', data.account.pk)
            return HttpResponseRedirect(
                reverse(
                    'admin_dashboard_accounts_detail',
                    kwargs={
                        'account': data.account.pk
                    }
                )
            )
        else:
            context = {
                "page_title": "Update Profile: {obj}",
                "menu_section": "admin_dashboard",
                "menu_subsection": "profile",
                "menu_action": "update",
                "obj": obj,
                "form": form
            }

            messages.error(
                request,
                'There were errors processing your request:',
                extra_tags='danger'
            )
            return render(request, "admin_dashboard/profiles/form.html", context)


class AdminDashboardProfileDeleteView(LoginRequiredMixin, IsAdminViewMixin, View):
    """ 
    Create view for Profiles. 
    
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
        obj = get_object_or_404(Master, pk=kwargs.get('profile', None))
        context = {
            "page_title": f"Delete Profile: {obj}",
            "menu_section": "admin_dashboard",
            "menu_subsection": "profile",
            "menu_action": "delete",
            "obj": obj
        }

        return render(request, "profiles/delete.html", context)
    
    def post(self, request, *args, **kwargs):
        obj = get_object_or_404(Master, pk=kwargs.get('profile', None))

        messages.success(
            request,
            f'{obj} deleted!',
            extra_tags='success'
        )

        obj.delete()

        return HttpResponseRedirect(
            reverse(
                'admin_dashboard_profiles_list'
            )
        )


class DashboardProfileUpdateView(LoginRequiredMixin, View):
    """ 
    Create view for Profiles. 
    
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
        obj = get_object_or_404(Master, pk=kwargs.get('profile', None))
        form = MasterForm(instance=obj)

        context = {
            "page_title": f"Update Profile: {obj}",
            "menu_section": "admin_dashboard",
            "menu_subsection": "profile",
            "menu_action": "update",
            "obj": obj,
            "form": form
        }

        return render(request, "dashboards/profiles/profile_form.html", context)
    
    def post(self, request, *args, **kwargs):
        obj = get_object_or_404(Master, pk=kwargs.get('profile', None))
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
            next = request.POST.get('next', '/')
            return HttpResponseRedirect(next)
        else:
            context = {
                "page_title": "Update Profile: {obj}",
                "menu_section": "admin_dashboard",
                "menu_subsection": "profile",
                "menu_action": "update",
                "obj": obj,
                "form": form
            }

            messages.error(
                request,
                'There were errors processing your request:',
                extra_tags='danger'
            )
            return render(request, "admin_dashboard/profiles/form.html", context)