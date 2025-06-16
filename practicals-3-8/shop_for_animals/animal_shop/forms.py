from django import forms
from .models import Comment, Order

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'text']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your name'}),
            'text': forms.Textarea(attrs={'placeholder': 'Your comment...'}),
        }

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer_name', 'customer_phone', 'customer_email', 'delivery_address', 'notes']
        widgets = {
            'customer_name': forms.TextInput(attrs={
                'placeholder': 'Full Name',
                'required': True
            }),
            'customer_phone': forms.TextInput(attrs={
                'placeholder': '+380 XX XXX XX XX',
                'required': True,
                'pattern': r'^\+?[\d\s\-\(\)]+$'
            }),
            'customer_email': forms.EmailInput(attrs={
                'placeholder': 'your.email@example.com'
            }),
            'delivery_address': forms.Textarea(attrs={
                'placeholder': 'Enter your full delivery address...',
                'rows': 3,
                'required': True
            }),
            'notes': forms.Textarea(attrs={
                'placeholder': 'Any special instructions for your order...',
                'rows': 2
            }),
        }
        labels = {
            'customer_name': 'Full Name',
            'customer_phone': 'Phone Number',
            'customer_email': 'Email Address',
            'delivery_address': 'Delivery Address',
            'notes': 'Order Notes (Optional)'
        }

    def clean_customer_phone(self):
        phone = self.cleaned_data.get('customer_phone')
        if phone:
            clean_phone = ''.join(filter(str.isdigit, phone))
            if len(clean_phone) < 10:
                raise forms.ValidationError('Please enter a valid phone number.')
        return phone