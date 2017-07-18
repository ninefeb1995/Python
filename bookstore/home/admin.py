from django.contrib import admin
from home import models

# Register your models here.
admin.site.register(models.Book)
admin.site.register(models.BookImage)
admin.site.register(models.Category)
#admin.site.register(models.User)
admin.site.register(models.Order)
admin.site.register(models.OrderDetail)

