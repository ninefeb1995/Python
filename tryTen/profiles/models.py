from __future__ import unicode_literals
from django.db import models
from django.conf import settings
from allauth.account.signals import user_logged_in
from allauth.account.signals import user_signed_up


# Create your models here.
class profile(models.Model):
    name = models.CharField(max_length=120)
    use = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, blank=True)
    description = models.TextField(default="Default text")
    location = models.CharField(max_length=120, default="Default location")
    job = models.CharField(max_length=120, null=True)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class userStripe(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    stripe_id = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        if self.stripe_id:
            return self.stripe_id
        else:
            return self.user.username

#
# def my_call_back(sender, **kwargs):
#     print("Request finished")
#     print(kwargs)
#
#
# user_logged_in.connect(my_call_back)


