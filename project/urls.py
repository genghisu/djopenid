from django.conf.urls.defaults import *

urlpatterns = patterns(
    '',
    ('^consumer/', include('consumer.urls')),
)
