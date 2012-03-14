from django.conf.urls.defaults import *

urlpatterns = patterns(
    'trade.views',
    url(r'^$', 'home', name='trade-home'),
    url(r'^init_trade_request/$', 'init_trade_request', name='init-trade-request'),
)
