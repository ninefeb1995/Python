from django.contrib import admin
from .models import profile
from .models import userStripe

class profileAdmin(admin.ModelAdmin):
    class Meta:
        model = profile


# Register your models here.
admin.site.register(profile, profileAdmin)


class userStripeAdmin(admin.ModelAdmin):
    class Meta:
        model = userStripe


admin.site.register(userStripe, userStripeAdmin)