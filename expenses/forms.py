from django import forms
from .models import Transaction
from django.contrib.auth.forms import UserCreationForm
from .models import User,Category, Feedback  # Import your custom User model

class TransactionForm(forms.ModelForm):
    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount<= 0:
            raise forms.ValidationError("How can you have negative transactions?")
        return amount
    
    class Meta:
        model = Transaction
        fields = ['date', 'category', 'type', 'amount', 'description']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'AAAA-MM-DD'}),
        }
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']  # Specify fields for the form


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['bio']  # Only include the bio field
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'textarea textarea-bordered h-24',
                'placeholder': 'Your feedback',
            }),
        }