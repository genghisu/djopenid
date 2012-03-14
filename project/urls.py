from django.conf.urls.defaults import *
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns(
    '',
    ('^consumer/', include('consumer.urls')),
    ('^trade/', include('trade.urls')),
)
