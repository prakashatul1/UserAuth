from django.conf.urls import url
from . import views
from django.contrib.auth.views import password_reset_done

app_name = 'accounts'

urlpatterns = [
    url(r'^login/$',views.loginview,name='login'),
    url(r'^logout/$',views.logoutview,name='logout'),
    url(r'^register/$', views.register, name='register' ),
    url(r'^profile/$', views.view_profile, name='profile'),
    url(r'^profile/view_all/$', views.view_all, name='view_all'),
    url(r'^profile/edit/$', views.edit_profile, name='edit_profile'),
    url(r'^profile/delete/$', views.delete_profile, name='delete_profile'),
    url(r'^change_password/$', views.change_password, name='change_password'),
    url(r'^reset_password/$',views.password_reset,name='password_reset'),
    url(r'^reset_password/done/$', password_reset_done, name='password_reset_done'),
    url(r'^password_reset/confirm/', views.password_reset_confirm,
        name='password_reset_confirm'),
]