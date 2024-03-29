import django.http as http
import django.shortcuts as shortcuts
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist

from trade.models import TradeRequest

def home(request):
    steam_id = request.session.get('steam_id', None)

    return shortcuts.render_to_response('trade/home.html',
                                        {'steam_id':steam_id},
                                        context_instance = RequestContext(request)) 
    
def init_trade_request(request):
    steam_id = request.session.get('steam_id', None)
    error = None
    if steam_id:
        trade_request = TradeRequest.objects.create_new(steam_id)
        if not trade_request:
            error = 'You have already requested a trade session, please conclude that before you initiate another trade'
    else:
        trade_request = None
        error = 'Valid steamid needed to initiate trade'
        
    return shortcuts.render_to_response('trade/init_trade_request.html',
                                        {'trade_request':trade_request,
                                         'error':error},
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