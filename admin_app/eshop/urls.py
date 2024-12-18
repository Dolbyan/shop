"""
URL configuration for eshop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include, re_path
from django.conf import settings
import os
from django.conf.urls.static import static
from gunicorn.app.pasterapp import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include("admin_app.app.urls")),
    path('favicon.ico', serve, {'document_root': os.path.join(settings.STATIC_ROOT, 'favicon.ico')}),
]


if settings.DEBUG:
    urlpatterns += static('favicon.ico', document_root=os.path.join(settings.BASE_DIR, 'admin_app/static'))