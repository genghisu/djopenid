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

class TradeRequest(models.Model):
    steam_id = models.TextField(default = '')
    date_created = CreationDateTimeField()
    processed = models.BooleanField(default = False)
    trade_session = models.ForeignKey(TradeSession)
    
class TradeBot(models.Model):
    TRADE_STATUS = (('BUSY', 'BUSY'), ('READY', 'READY'))
    
    name = models.TextField()
    ip = models.TextField()
    trade_status = models.CharField(max_length = 75, choices = TRADE_STATUS)