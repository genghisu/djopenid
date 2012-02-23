
from django.conf.urls.defaults import *

urlpatterns = patterns(
    'consumer.views',
    (r'^$', 'startOpenID'),
    (r'^finish/$', 'finishOpenID'),
    (r'^settings/$', 'serverSettings'),
)
