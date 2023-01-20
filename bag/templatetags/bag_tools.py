from django import template


register = template.Library()       #creating custom tag filters in DJANGO


@register.filter(name='calc_subtotal')
def calc_subtotal(price, quantity):
    return price * quantity