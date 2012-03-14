import socket

from django.conf import settings
from django.core import management
from django.core.management.base import NoArgsCommand
from django.core.exceptions import ObjectDoesNotExist

from trade.models import TradeRequest, TradeSession

class Command(NoArgsCommand):
    help = ""

    requires_model_validation = True
    can_import_settings = True
    
    def handle(self, *test_labels, **options):
        HOST = '10.112.49.144'                 # Symbolic name meaning all available interfaces
        PORT = 50000              # Arbitrary non-privileged port
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((HOST, PORT))
        print "Listening for socket connection"
        s.listen(1)
        conn, addr = s.accept()
        print 'Connected by', addr
        while 1:
            data = conn.recv(1024)
            if data:
                handle_incoming_data(data)
            trade_requests = TradeRequest.objects.filter(processed = False)
            if trade_requests:
                outgoing_data = [tr.as_dict() for tr in trade_requests]
                connect.sendall(str(outgoing_data))
                print "Sending: %s" % (str(outgoing_data))
                for trade_request in trade_requests:
                    trade_request.processed = True
                    trade_request.save()
                    
    def handle_incoming_data(self, data):
        print data