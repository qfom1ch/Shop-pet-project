from .models import OrderItem


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_descriptions(descriptions):
    res = []
    for item in descriptions:
        res.append(item[0] + ' - ' + str(item[1]) + ' шт.')
    return ' '.join(res)


def quantity_minus_order_quantity(order):
    order_items = OrderItem.objects.filter(order=order)
    for item in order_items:
        item.product.quantity -= item.quantity
        item.product.save()
