from django.conf.urls import url
from serv import views

urlpatterns = [
	url(r'^$', views.home_view),
    url(r'^login/$', views.login_view),
    url(r'^logout/$', views.logout_view),
    url(r'^key_list/$', views.key_list_view),
    url(r'^user_admin/$', views.user_admin_view),
    url(r'^user_request/$', views.user_request_view),
	url(r'^user_request_success/$', views.user_request_success_view),
    url(r'^download_config/(?P<key_name>\S+)$', views.download_config_view),
]
