def cart_context(request):
    from .models import Cart

    if request.user.is_authenticated:
        items = Cart.objects.filter(user=request.user).select_related("product")
    elif request.session.session_key:
        items = Cart.objects.filter(session_key=request.session.session_key).select_related("product")
    else:
        items = Cart.objects.none()

    count = sum(item.quantity for item in items)
    total = sum(item.subtotal for item in items)

    return {
        "cart_count": count,
        "cart_total": total,
    }
