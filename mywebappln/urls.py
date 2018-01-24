"""mywebappln URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls import url, include
from django.contrib import admin
from accounts import views

urlpatterns = [
    url(r'^$', views.loginview),
    url(r'^admin/', admin.site.urls),
    url(r'^account/',include('accounts.urls')),
    url(r'^userprofile/$', views.UserProfileList.as_view()),
    url(r'^userprofile/(?P<pk>[0-9]+)/$',
        views.DetailsView.as_view(), name="details"),
    # custom api
    # url(r'^api/userprofile/$',views.userprofileapiview,name='userprofile_api'),
    # url(r'^api/userprofile/(?P<pk>[0-9]+)/$',views.userdetailapiview,name='userdetail_api')
]
urlpatterns = format_suffix_patterns(urlpatterns)