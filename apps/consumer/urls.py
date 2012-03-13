
from django.conf.urls.defaults import *

urlpatterns = patterns(
    'consumer.views',
    (r'^$', 'startOpenID'),
    url(r'^start_with_target/(?P<target>.+)/$', 'startOpenID', name='start-OpenID-site'),
    (r'^finish/$', 'finishOpenID'),
    url('r^finish/(?P<target>.+)/$', 'finishOpenID', name='finish-OpenID-with-target'),
    (r'^settings/$', 'serverSettings'),
)
