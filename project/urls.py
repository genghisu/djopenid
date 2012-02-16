from django.conf.urls.defaults import *

urlpatterns = patterns(
    '',
    ('^$', 'core.views.index'),
    ('^consumer/', include('consumer.urls')),
    ('^server/', include('server.urls')),
)
