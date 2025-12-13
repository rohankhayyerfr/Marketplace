from django.contrib import messages
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
    if request.method != "POST":
        return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

    try:
        if not request.body:
            return JsonResponse({'status': 'error', 'message': 'Empty request body'}, status=400)

        data = json.loads(request.body)

        product_id = data.get('product_id')
        variant_id = data.get('variant_id')
        quantity = int(data.get('quantity', 1))

        if quantity < 1:
            quantity = 1

        product = get_object_or_404(Product, id=product_id)

        variant = None
        if variant_id:
            variant = get_object_or_404(ProductVariant, id=int(variant_id))

        # CART
        if request.user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(user=request.user)
        else:
            session = request.session.session_key
            if not session:
                request.session.create()
                session = request.session.session_key
            cart, _ = Cart.objects.get_or_create(session_id=session)

        # جلوگیری از تکراری شدن آیتم
        item = CartItem.objects.filter(cart=cart, product=product, variant=variant).first()

        if item:
            item.quantity += quantity
            item.save()
        else:
            item = CartItem.objects.create(
                cart=cart,
                product=product,
                variant=variant,
                quantity=quantity
            )

        return JsonResponse({
            'status': 'success',
            'message': "به سبد خرید اضافه شد",
            'item_id': item.pk,
            'quantity': item.quantity
        })

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)




def update_cart_item(request):
    if request.method == "POST":
        item_id = request.POST.get("item_id")
        delta = int(request.POST.get("delta"))

        try:
            item = CartItem.objects.get(id=item_id)
            item.quantity += delta

            if item.quantity < 1:
                item.quantity = 1

            item.save()


            return JsonResponse({"success": True})
        except:
            return JsonResponse({"success": False})

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

