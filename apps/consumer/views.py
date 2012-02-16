import json

from django import http
from django.http import HttpResponseRedirect
from django.views.generic.simple import direct_to_template
from django.conf import settings
import django.shortcuts as shortcuts
from django.template import RequestContext
from django.core.urlresolvers import reverse

from openid.consumer import consumer
from openid.consumer.discover import DiscoveryFailure
from openid.extensions import ax, pape, sreg
from openid.yadis.constants import YADIS_HEADER_NAME, YADIS_CONTENT_TYPE
from openid.server.trustroot import RP_RETURN_TO_URL_TYPE

from core import util

PAPE_POLICIES = [
    'AUTH_PHISHING_RESISTANT',
    'AUTH_MULTI_FACTOR',
    'AUTH_MULTI_FACTOR_PHYSICAL',
    ]

# List of (name, uri) for use in generating the request form.
POLICY_PAIRS = [(p, getattr(pape, p))
                for p in PAPE_POLICIES]

def getOpenIDStore():
    """
    Return an OpenID store object fit for the currently-chosen
    database backend, if any.
    """
    return util.getOpenIDStore('/tmp/djopenid_c_store', settings.OPENID_TABLE_PREFIX)

def getConsumer(request):
    """
    Get a Consumer object to perform OpenID authentication.
    """
    return consumer.Consumer(request.session, getOpenIDStore())

def renderIndexPage(request, **template_args):
    template_args['consumer_url'] = util.getViewURL(request, startOpenID)
    template_args['pape_policies'] = POLICY_PAIRS

    response =  direct_to_template(
        request, 'consumer/index.html', template_args)
    response[YADIS_HEADER_NAME] = util.getViewURL(request, rpXRDS)
    return response

def startOpenID(request):
    """
    Start the OpenID authentication process.  Renders an
    authentication form and accepts its POST.

    * Renders an error message if OpenID cannot be initiated

    * Requests some Simple Registration data using the OpenID
      library's Simple Registration machinery

    * Generates the appropriate trust root and return URL values for
      this application (tweak where appropriate)

    * Generates the appropriate redirect based on the OpenID protocol
      version.
    """
    openid_url = settings.OPENID_URL
    c = getConsumer(request)
    error = None

    try:
        auth_request = c.begin(openid_url)
    except DiscoveryFailure, e:
        # Some other protocol-level failure occurred.
        error = "OpenID discovery error: %s" % (str(e),)

    if error:
        # Render the page with an error.
        return renderIndexPage(request, error=error)

    # Add Simple Registration request information.  Some fields
    # are optional, some are required.  It's possible that the
    # server doesn't support sreg or won't return any of the
    # fields.
    sreg_request = sreg.SRegRequest(optional=['email', 'nickname'],
                                    required=['dob'])
    auth_request.addExtension(sreg_request)

    # Add Attribute Exchange request information.
    ax_request = ax.FetchRequest()
    # XXX - uses myOpenID-compatible schema values, which are
    # not those listed at axschema.org.
    ax_request.add(
        ax.AttrInfo('http://schema.openid.net/namePerson',
                    required=True))
    ax_request.add(
        ax.AttrInfo('http://schema.openid.net/contact/web/default',
                    required=False, count=ax.UNLIMITED_VALUES))
    auth_request.addExtension(ax_request)

    # Add PAPE request information.  We'll ask for
    # phishing-resistant auth and display any policies we get in
    # the response.
    requested_policies = []
    policy_prefix = 'policy_'
    for k, v in request.POST.iteritems():
        if k.startswith(policy_prefix):
            policy_attr = k[len(policy_prefix):]
            if policy_attr in PAPE_POLICIES:
                requested_policies.append(getattr(pape, policy_attr))

    if requested_policies:
        pape_request = pape.Request(requested_policies)
        auth_request.addExtension(pape_request)

    # Compute the trust root and return URL values to build the
    # redirect information.
    trust_root = util.getViewURL(request, startOpenID)
    return_to = util.getViewURL(request, finishOpenID)

    # Send the browser to the server either by sending a redirect
    # URL or by generating a POST form.
    url = auth_request.redirectURL(trust_root, return_to)
    return HttpResponseRedirect(url)

def finishOpenID(request):
    """
    Finish the OpenID authentication process.  Invoke the OpenID
    library with the response from the OpenID server and render a page
    detailing the result.
    """
    result = {}

    # Because the object containing the query parameters is a
    # MultiValueDict and the OpenID library doesn't allow that, we'll
    # convert it to a normal dict.

    # OpenID 2 can send arguments as either POST body or GET query
    # parameters.
    errors = []
    request_args = request.GET

    
    if request.method == 'POST':
        request_args.update(util.normalDict(request.POST))

    if request_args:
        c = getConsumer(request)

        # Get a response object indicating the result of the OpenID
        # protocol.
        return_to = util.getViewURL(request, finishOpenID)
        response = c.complete(request_args, return_to)

        # Get a Simple Registration response object if response
        # information was included in the OpenID response.
        sreg_response = {}
        ax_items = {}
        if response.status == consumer.SUCCESS:
            sreg_response = sreg.SRegResponse.fromSuccessResponse(response)

            ax_response = ax.FetchResponse.fromSuccessResponse(response)
            if ax_response:
                ax_items = {
                    'fullname': ax_response.get(
                        'http://schema.openid.net/namePerson'),
                    'web': ax_response.get(
                        'http://schema.openid.net/contact/web/default'),
                    }

        # Get a PAPE response object if response information was
        # included in the OpenID response.
        pape_response = None
        if response.status == consumer.SUCCESS:
            pape_response = pape.Response.fromSuccessResponse(response)

            if not pape_response.auth_policies:
                pape_response = None

        # Map different consumer status codes to template contexts.
        results = {
            consumer.CANCEL:
            {'message': 'OpenID authentication cancelled.'},

            consumer.FAILURE:
            {'error': 'OpenID authentication failed.'},

            consumer.SUCCESS:
            {'url': response.getDisplayIdentifier(),
             'sreg': sreg_response and sreg_response.items(),
             'ax': ax_items.items(),
             'pape': pape_response}
            }

        result = results[response.status]

        if isinstance(response, consumer.FailureResponse):
            # In a real application, this information should be
            # written to a log for debugging/tracking OpenID
            # authentication failures. In general, the messages are
            # not user-friendly, but intended for developers.
            result['failure_reason'] = response.message
    
    if 'openid.claimed_id' in request_args.keys():
        steamid = request_args.get('openid.claimed_id').split('/')[-1]
    else:
        errors.append('OPENID_FAILURE')

    response = {'response': json.dumps({'errors':errors, 'steamid':steamid})}
            
    return shortcuts.render_to_response('json.html',
                                    response,
                                    context_instance = RequestContext(request),
                                    mimetype = "application/json")

def rpXRDS(request):
    """
    Return a relying party verification XRDS document
    """
    return util.renderXRDS(
        request,
        [RP_RETURN_TO_URL_TYPE],
        [util.getViewURL(request, finishOpenID)])
