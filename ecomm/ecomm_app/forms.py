from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser,Color,Order, ShippingMethod,PaymentMethod

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2','first_name','last_name','address','contact']

class CustomLoginForm(AuthenticationForm):
    class Meta:
        fields = ['username', 'password']
        
class ContactUsForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    subject = forms.CharField(max_length=200, required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)
    
class ProductColorSelectionForm(forms.Form):
    color = forms.ModelChoiceField(queryset=Color.objects.all(), widget=forms.Select)
    
class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['billing_address', 'shipping_address', 'shipping_method', 'payment_method']

    shipping_method = forms.ModelChoiceField(queryset=ShippingMethod.objects.all(), empty_label=None)
    payment_method = forms.ModelChoiceField(queryset=PaymentMethod.objects.all(), empty_label=None)


    def clean_shipping_address(self):
        address = self.cleaned_data.get('shipping_address')
        if not address:
            raise forms.ValidationError("Shipping address is required.")
        return address

    def clean_billing_address(self):
        address = self.cleaned_data.get('billing_address')
        if not address:
            raise forms.ValidationError("Billing address is required.")
        return address
    


        