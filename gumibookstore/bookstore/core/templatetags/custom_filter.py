from  django import template
from books import models
from carts import models

register = template.Library()


@register.filter()
def detail_100_characters(detail_str):
    return detail_str[0:101] + "." * 50

@register.filter
def get_status_name(status, cart_id):
    return status.get(cart_id).upper()


