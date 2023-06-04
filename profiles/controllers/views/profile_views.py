from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View

from accounts.controllers.views.account.forms.account_forms import AccountUpdateForm, UpdatePasswordForm
from .forms.profile_forms import ProfileForm
from profiles.models import Profile
from accounts.models import Account
from accounts.models.account.constants import SUPERADMIN, ADMIN, USER
from loans.models.loan.models import Loan
from loans.models.loan_type.models import LoanType
from payments.models.payment_request.models import PaymentRequest


class ProfileHomeView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        try:
            profile = request.user.profile
            context = {
                'page_title': f'{profile} profile',
                'profile': profile
            }

            return render(request, 'dashboards/profiles/home.html', context)
        except:
            messages.error(request, 'Account profile unavailable', extra_tags='danger')
            users = Account.objects.filter(user_type=USER)
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
            previous_page = request.META.get('HTTP_REFERER')
            return redirect(previous_page)
        
        


class ProfileUpdateView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        profile = request.user.profile
        form = ProfileForm(instance=profile)

        context = {
            'page_title': f'Update {profile} profile',
            'form': form,
            'profile': profile
        }

        return render(request, 'dashboards/profiles/profile_form.html', context)

    def post(self, request, *args, **kwargs):
        profile = request.user.profile
        form = ProfileForm(instance=profile, data=request.POST)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            messages.success(request, f"{obj} updated!", extra_tags='success')
            return HttpResponseRedirect(reverse('profile_home_view'))
        else:
            messages.error(request, form.errors, extra_tags='danger')
            context = {
                'page_title': f'Update {profile} profile',
                'form': form,
                'profile': profile
            }
            return render(request, 'dashboards/profiles/profile_form.html', context)


class AccountUpdateView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = request.user
        form = AccountUpdateForm(instance=user)

        context = {
            'page_title': f'Update {user} account',
            'form': form,
            'user': user
        }

        return render(request, 'dashboards/profiles/account_form.html', context)

    def post(self, request, *args, **kwargs):
        user = request.user
        form = AccountUpdateForm(instance=user, data=request.POST)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            messages.success(request, f"{obj} updated!", extra_tags='success')
            return HttpResponseRedirect(reverse('profile_home_view'))
        else:
            messages.error(request, form.errors, extra_tags='danger')
            context = {
                'page_title': f'Update {user} account',
                'form': form,
                'user': user
            }
            return render(request, 'dashboards/profiles/account_form.html', context)


class AccountPasswordUpdateView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = request.user
        form = UpdatePasswordForm

        context = {
            'page_title': f'Update {user} password',
            'form': form,
            'user': user
        }

        return render(request, 'dashboards/profiles/account_form.html', context)

    def post(self, request, *args, **kwargs):
        user = request.user
        form = UpdatePasswordForm(data=request.POST)

        if form.is_valid():
            user.set_password(form.cleaned_data.get('password'))
            user.save()
            messages.success(request, f"Password updated!", extra_tags='success')
            return HttpResponseRedirect(reverse('profile_home_view'))
        else:
            messages.error(request, form.errors, extra_tags='danger')
            context = {
                'page_title': f'Update {user} account',
                'form': form,
                'user': user
            }
            return render(request, 'dashboards/profiles/account_form.html', context)
