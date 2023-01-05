"""servioPayroll URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from accounts.controllers.views.account.main import AccountLoginView
from accounts.models.account.constants import ADMIN_URL

URL_READ_ONLY = {
    'get': 'list'
}

URL_DETAIL = {
    'get': 'retrieve'
}

URL_CREATE = {
    'get': 'list',
    'post': 'create',
}

URL_UPDATE = {
    'get': 'retrieve',
    'put': 'update',
    # 'patch': 'update_partial'
}

URL_DELETE = {
    'get': 'retrieve',
    'delete': 'destroy'
}

urlpatterns = [
    path('', AccountLoginView.as_view(), name='root'),
    path(ADMIN_URL, admin.site.urls),

    path('profile/', include('profiles.urls')),
    path('accounts/', include('accounts.urls')),
    path('locations/', include('locations.urls')),
    path('loans/', include('loans.urls')),
    path('amortizations/', include('amortizations.urls')),
    path('payments', include('payments.urls')),

    # dashboards
    path('admin/', include('admin_dashboard.urls')),
    path('user/', include('user_dashboard.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    from rest_framework import permissions
    from drf_yasg.views import get_schema_view
    from drf_yasg import openapi

    schema_view = get_schema_view(
        openapi.Info(
            title="ISMILE Server API",
            default_version='v1',
            description="API for ISMILE",
            terms_of_service="/policies/terms/",
            contact=openapi.Contact(email="markjungersaniva@gmail.com"),
            # license=openapi.License(name="BSD License"),
        ),
        public=False,
        permission_classes=(permissions.AllowAny,),
    )

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
        url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
        url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
        url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    ]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
