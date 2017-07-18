from  django import template
from home import models

register = template.Library()


@register.filter()
def detail_100_characters(detail_str):
    return detail_str[0:101] + "." * 50

# @register.filter()
# def get_book_in_order(book_id):
#     return  models.Book.objects.get(id=book_id)

