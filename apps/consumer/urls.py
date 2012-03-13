
from django.conf.urls.defaults import *

urlpatterns = patterns(
    'consumer.views',
    (r'^$', 'startOpenID'),
    url(r'^start_site/$', 'start_OpenID_site', name = 'start-OpenID-site'),
    url(r'^finish_site/$', 'finish_OpenID_site', name='finish-OpenID-site'),
    (r'^finish/$', 'finishOpenID'),
    (r'^settings/$', 'serverSettings'),
)
