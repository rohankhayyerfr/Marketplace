from django import forms

class CheckoutForm(forms.Form):
    full_name = forms.CharField(max_length=100, label='نام و نام خانوادگی')
    email = forms.EmailField(label='ایمیل')
    phone = forms.CharField(max_length=15, label='شماره تماس')
    address = forms.CharField(widget=forms.Textarea, label='آدرس ارسال')