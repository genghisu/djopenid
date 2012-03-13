import django.http as http
import django.shortcuts as shortcuts
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist

from trade.models import TradeRequest

def home(request):
    steamid = request.session.get('steamid', None)

    return shortcuts.render_to_response('trade/home.html',
                                        {'steamid':steamid},
                                        context_instance = RequestContext(request)) 
def steam_login(request):
    pass

def init_trade_request(request):
    if request.POST:
        steam_id = request.POST.get('steam_id', None)
        trade_request = TradeRequest.add_new_request(steam_id)
    
    return shortcuts.render_to_response('trade/init_trade_request.html',
                                        {'trade_request':trade_request},
                                        context_instance = RequestContext(request))

def check_trade_request(request, trade_request_id):
    trade_request = TradeRequest.objects.get(id = int(trade_request_id))
    
    return shortcuts.render_to_response('trade/check_trade_request.html',
                                        {'trade_request':trade_request},
                                        context_instance = RequestContext(request))
    
def check_trade_session(request, trade_session_id):
    trade_request = TradeRequest.objects.get(id = int(trade_request_id))
    
    return shortcuts.render_to_response('trade/check_trade_request.html',
                                        {'trade_request':trade_request},
                                        context_instance = RequestContext(request))