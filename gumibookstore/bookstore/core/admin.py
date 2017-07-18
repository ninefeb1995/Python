from django.contrib import admin
from books.models import *
from carts.models import *
from orders.models import *


class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'condition', 'inventory', 'image')
    search_fields = ['title']
    list_editable = ('condition', 'inventory', 'image')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('cart', 'user', 'status', 'begin_date', 'end_date')
    list_editable = ('status', 'end_date')


class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'item')


admin.site.register(Book, BookAdmin)
admin.site.register(Category)
admin.site.register(Author)
admin.site.register(Publisher)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Cart)
admin.site.register(Order, OrderAdmin)
