from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from store.models import Product, ProductVariant
from .models import Cart, CartItem
import json
def get_cart(request):
    session = request.session.session_key
    if not session:
        request.session.create()
        session = request.session.session_key

    cart, created = Cart.objects.get_or_create(session_id=session)
    return cart

def add_to_cart(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            product_id = int(data.get('product_id'))
            variant_id = data.get('variant_id')
            quantity = int(data.get('quantity', 1))

            # محصول
            product = get_object_or_404(Product, id=product_id)

            # واریانت
            variant = None
            if variant_id:
                variant = get_object_or_404(ProductVariant, id=int(variant_id))

            # گرفتن سبد خرید (بر اساس session یا user)
            if request.user.is_authenticated:
                cart, created = Cart.objects.get_or_create(user=request.user)
            else:
                session = request.session.session_key
                if not session:
                    request.session.create()
                    session = request.session.session_key
                cart, created = Cart.objects.get_or_create(session_id=session)

            # اضافه کردن به cartitem
            item, created_item = CartItem.objects.get_or_create(
                cart=cart,
                product=product,
                variant=variant,
                defaults={'quantity': quantity}
            )

            if not created_item:
                item.quantity += quantity
                item.save()

            return JsonResponse({
                'status': 'success',
                'message': "به سبد خرید اضافه شد",
                'item_id': item.id,
                'quantity': item.quantity
            })

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


def update_cart_item(request):
    if request.nethod == 'POST':
        item_id = request.POST.get('item_id')
        delta = int(request.POST.get('delta', 0))
        item = get_object_or_404(CartItem, id=item_id)
        item.quantity += delta
        if item.quantity < 1:
            item.quantity = 1
        item.save()
        return JsonResponse({'success': True, 'quantity': item.quantity, 'total_price': item.total_price})
    return JsonResponse({'success': False}, status=400)

def remove_cart_item(request):
    if request.method == "POST":
        item_id = request.POST.get('item_id')
        item = get_object_or_404(CartItem, id=item_id)
        item.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)
def cart_home(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
    else:
        session = request.session.session_key
        if not session:
            cart = None
        else:
            cart = Cart.objects.filter(session_id=session).first()

    return render(request, 'cart/cart.html', {'cart': cart})
