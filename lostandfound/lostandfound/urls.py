"""lostandfound URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from lostfoundapp.views import report_missing_item, landing_page, missing_item_detail, signup_page, login_page, missing_items_list
urlpatterns = [
    path("admin/", admin.site.urls),
    path('report-missing-item/', report_missing_item, name='report_missing_item'),
    path('', landing_page, name='landing_page'),
    path('sign-up/', signup_page, name='signup_page'),
    path('log-in/', login_page, name='login_page'),
    path('missing-item/<int:item_id>/',
         missing_item_detail, name='missing_item_detail'),
    path('missing-items/', missing_items_list, name='missing_items_list'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
