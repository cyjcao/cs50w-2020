from django import template

register = template.Library()

@register.filter
def current_price(listing):
    """
    Return updated current price of listing
    """
    return listing.bids.order_by('-amount').first().amount

    
