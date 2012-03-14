from django.db import models
from django.contrib.contenttypes.models import ContentType

from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField
    
class TradeSession(models.Model):
    trade_initiated = models.BooleanField(default = False)
    trade_accepted = models.BooleanField(default = False)
    done = models.BooleanField(default = False)
    trade_successful = models.BooleanField(default = False)
    date_created = CreationDateTimeField()
    date_modified = ModificationDateTimeField()

class TradeRequestManager(models.Manager):
    def create_new(self, steam_id):
        trade_request = None
        if not TradeRequest.objects.filter(steam_id = steam_id, processed = False):
            trade_session = TradeSession()
            trade_session.save()
            trade_request = TradeRequest(steam_id = steam_id, trade_session = trade_session)
            trade_request.save()
        return trade_request
        
class TradeRequest(models.Model):
    steam_id = models.TextField(default = '')
    date_created = CreationDateTimeField()
    processed = models.BooleanField(default = False)
    trade_session = models.ForeignKey(TradeSession)
    objects = TradeRequestManager()
    
    def as_dict(self):
        return {'steam_id':str(self.steam_id),
                'id':str(self.id)}
        
class TradeBot(models.Model):
    TRADE_STATUS = (('BUSY', 'BUSY'), ('READY', 'READY'))
    
    name = models.TextField()
    ip = models.TextField()
    trade_status = models.CharField(max_length = 75, choices = TRADE_STATUS)