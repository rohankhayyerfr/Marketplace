from .models import Cart, CartItem

def cart_item_count(request):
    try:
        if request.user.is_authenticated:
            cart = Cart.objects.filter(user=request.user).first()
        else:
            session = request.session.session_key
            if not session:
                return {'cart_count': 0}

            cart = Cart.objects.filter(session_id=session).first()

        if not cart:
            return {'cart_count': 0}

        count = CartItem.objects.filter(cart=cart).count()
        return {'cart_count': count}

    except:
        return {'cart_count': 0}