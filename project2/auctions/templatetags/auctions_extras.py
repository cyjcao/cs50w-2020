from django import template

register = template.Library()

@register.filter
def current_price(listing):
    return listing.bids.order_by('-amount').first().amount

    
