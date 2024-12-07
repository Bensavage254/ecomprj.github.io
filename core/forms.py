from django import forms
from core.models import ProductReview

class ProductReviewForm(forms.ModelForm):
    review = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Write review'}))

    class Meta:
        model = ProductReview
        fields = ['review', 'rating']

class PaymentForm(forms.Form):
    phone_number = forms.CharField(max_length=15, label='Phone Number')
    amount = forms.IntegerField(label='Amount', min_value=1)