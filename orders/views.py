import json

import requests
from django.shortcuts import render, redirect, get_object_or_404

from django.conf import settings
from .models import Order, OrderItem
from .forms import CheckoutForm
from store.models import Product
from cart.models import Cart


def checkout(request):
    # پیدا کردن سبد خرید کاربر یا session
    if request.user.is_authenticated:
        cart = get_object_or_404(Cart, user=request.user)
    else:
        session_id = request.session.session_key
        if not session_id:
            request.session.create()
            session_id = request.session.session_key
        cart = get_object_or_404(Cart, session_id=session_id)

    if request.method == 'POST':

        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        payment_method = request.POST.get('payment_method')

        # ایجاد سفارش
        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            total_price=cart.final_total,
            full_name=full_name,
            email=email,
            phone=phone,
            address=address,
            payment_status='pending'  # وضعیت اولیه سفارش
        )

        # افزودن آیتم‌ها به سفارش
        for item in cart.items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.total_price
            )

        # آماده کردن اطلاعات برای درگاه
        data = {
            "merchantID": "TEST",  # شناسه فروشنده
            "amount": order.total_price,  # مبلغ کل به تومان یا ریال
            "callbackURL": request.build_absolute_uri(f"/orders/payment-callback/{order.id}/"),  # URL بازگشت
            "orderId": str(order.id),  # شناسه سفارش
        }

        # URL درگاه (sandbox یا production)
        url = settings.PAYMENT_GATEWAY_URL
        payload = json.dumps(data)
        headers = {
            'Content-Type': 'application/json'
        }
        # ارسال درخواست به درگاه
        response = requests.post(url, json=data)
        result = response.json()
        response = requests.post(url, data=payload, headers=headers)

        response_content = response.json()
        print(response_content)
        if result.get("status") == "success":
            # درگاه یک لینک پرداخت یا token برمیگردونه
            payment_url = result.get("paymentURL")
            # حذف سبد خرید بعد از ایجاد سفارش
            cart.delete()
            # هدایت کاربر به صفحه پرداخت
            return redirect(payment_url)

        else:
            # خطا در ایجاد پرداخت
            context = {
                "cart": cart,
                "error": result.get("message", "خطا در اتصال به درگاه پرداخت")
            }
            return render(request, 'order/checkout.html', context)

    return render(request, 'order/checkout.html', {'cart': cart})




# orders/views.py
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'order/success.html', {'order': order})

def payment_callback(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    # verify پرداخت
    order.status = 'paid'
    order.payment_status = 'paid'
    order.save()