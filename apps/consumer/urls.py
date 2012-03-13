
from django.conf.urls.defaults import *

urlpatterns = patterns(
    'consumer.views',
    (r'^$', 'startOpenID'),
    url(r'^start/(?P<target>.+)/$', 'startOpenIDWithTarget', name='start-OpenID'),
    url(r'^finish/(?P<target>.+)/$', 'finishOpenID', name='finish-OpenID'),
    (r'^settings/$', 'serverSettings'),
)
