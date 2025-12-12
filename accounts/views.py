from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import SellerVerificationForm
from store.forms import EditProfileForm
from .models import SellerVerification


def user_register(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        username = request.POST.get("username")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")

        # چک کردن تکراری نبودن نام کاربری
        if User.objects.filter(username=username).exists():
            messages.error(request, "این نام کاربری قبلاً استفاده شده است")
            return redirect("accounts:register")

        # چک کردن تکراری نبودن ایمیل
        if User.objects.filter(email=email).exists():
            messages.error(request, "این ایمیل قبلاً استفاده شده است")
            return redirect("accounts:register")

        # چک تطابق رمزها
        if password != password2:
            messages.error(request, "رمز عبور و تکرار آن یکسان نیستند")
            return redirect("accounts:register")

        # ساخت کاربر
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        if not request.POST.get("terms"):
            messages.error(request, "باید قوانین را بپذیرید")
            return redirect("accounts:register")

        # لاگین خودکار بعد از ثبت‌نام
        login(request, user)
        return redirect("store:dashboard")

    return render(request, "accounts/register.html")
@login_required
def verify_identity(request):
    # این خط رکورد موجود یا جدید رو میاره
    sv, created = SellerVerification.objects.get_or_create(user=request.user)

    if request.method == "POST":
        # همیشه instance=sv پاس بده تا آپدیت انجام بشه نه insert
        form = SellerVerificationForm(request.POST, request.FILES, instance=sv)
        if form.is_valid():
            form.save()
            return redirect("accounts:verify_status")
    else:
        form = SellerVerificationForm(instance=sv)

    return render(request, 'accounts/verfication_identity.html', {
        'form': form,
        'identity': sv
    })


@login_required
def edit_identity(request):
    try:
        sv = request.user.sellerverification
    except SellerVerification.DoesNotExist:
        return redirect("accounts:verify_identity")

    if sv.status != "approved":
        messages.error(request, "هویت شما تایید شده است. امکان ویرایش وجود ندارد")
        return redirect("accounts:verify_identity")


    if request.method == "POST":
        form = SellerVerificationForm(request.POST, request.FILES, instance=sv)
        if form.is_valid():
            form.save()
            messages.success(request, "اطلاعات شما با موفقیت ویرایش شد!")
            return redirect("store:dashboard")
    else:
        form = SellerVerificationForm(instance=sv)

    return render(request, "accounts/edit_verify.html", {"form": form, "identity": sv})



@login_required
def verification_status(request):
    sv = getattr(request.user, "seller_verification", None)
    return render(request, "accounts/verfication_status.html", {"identity": sv})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('store:dashboard')
        else:
            messages.error(request, 'رمز یا نام کاربری اشتباه است')
            return redirect('accounts:login')

    return render(request, 'accounts/login.html')


def user_logout(request):
    logout(request)
    return redirect('store:home')

@login_required
def edit_profile(request):
    user = request.user
    if request.method == "POST":
        form = EditProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "اطلاعات شما با موفقیت بروزرسانی شد")
            return redirect("store:dashboard")
        else:
            messages.error(request, "لطفاً خطاهای فرم را بررسی کنید")
    else:
        form = EditProfileForm(instance=user)

    return render(request, 'accounts/edit_profile.html', {'user_form': form})