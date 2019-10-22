"""project URL Configuration

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
from django.contrib import admin
from django.urls import re_path, include, path
from rest_framework_jwt.views import obtain_jwt_token
from django.conf import settings
from django.views.generic import TemplateView
from django.shortcuts import render
from django.conf import settings
from django.conf.urls.static import static


def handler404(request, exception):
    return render(request, 'index.html', status=404)


handler404 = handler404

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include([
        path('api-token-auth/', obtain_jwt_token),
        path('rest-auth/', include('rest_auth.urls')),
        path('app/', include([
            path('inventory/', include('inventory.api.urls', namespace='inventory'), name='inventory'),
            path('bill/', include('bill.api.urls', namespace='bill'), name='bill'),
            path('menu/', include('menu.api.urls', namespace='menu'), name='menu'),
            path('sumup/', include('sumup.api', namespace='sumup'), name='sumup'),
        ]), name='app'),
    ])),
    re_path(r"^$", TemplateView.as_view(template_name='index.html')),
]

if settings.DEBUG is True:
    import debug_toolbar
    urlpatterns.append(path('__debug__/', include(debug_toolbar.urls)))

if settings.DEBUG is False:
    urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

print(settings.DEBUG)
