from allauth.account.signals import email_confirmed
from django.dispatch import receiver
from django.contrib.auth.models import Group, User
from fileupload.models import Item
from django.db import models
import re

@receiver(email_confirmed)
def registerNetworks(sender, **kwargs):
    emailDomain = re.search('[@.](\w+)\.edu$',kwargs['email_address'].email)
    if emailDomain:
        domain = emailDomain.group(1)
        if domain in ['stanford']:
            g, created = Group.objects.get_or_create(name=domain)
            if created:
                kwargs['email_address'].user.groups.add(g)

class Community(models.Model):
    group = models.OneToOneField(Group)
    requiredDomainEmail = models.CharField(max_length=40, blank=True, null=True, unique=True)

class Bid(models.Model):
    bidUser = models.ForeignKey(User, related_name='placedBids')
    bidPrice = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    bidTime = models.DateTimeField(auto_now=True)
    itemUser = models.ForeignKey(User, related_name='receivedBids')
    item = models.ForeignKey(Item)
    status = models.CharField(max_length=10, default='-', blank=False, null=False)

    class Meta:
        unique_together = (('bidUser', 'item'),)


class Link(models.Model):
    fromUser = models.ForeignKey(User, related_name='linkFrom')
    toUser = models.ForeignKey(User, related_name='linkTo')

    class Meta:
        unique_together = (('fromUser', 'toUser'),)