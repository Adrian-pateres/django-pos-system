from django import forms
from django.forms import inlineformset_factory
from django.core.exceptions import ValidationError
from .models import Product, Transaction, TransactionItem

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'stock']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'price': forms.NumberInput(attrs={'step': '0.01'}),
            'stock': forms.NumberInput(),
        }

class TransactionForm(forms.ModelForm):
    """
    Only capture the teller here. total_amount is computed in the view
    after validating the TransactionItem formset.
    """
    class Meta:
        model = Transaction
        fields = ['teller']
        widgets = {
            'teller': forms.HiddenInput(),
        }

class TransactionItemForm(forms.ModelForm):
    class Meta:
        model = TransactionItem
        fields = ['product', 'quantity']
        widgets = {
            'quantity': forms.NumberInput(attrs={'min': 1}),
        }

    def clean_quantity(self):
        qty = self.cleaned_data.get('quantity')
        if qty is None or qty <= 0:
            raise ValidationError("Quantity must be a positive number.")
        return qty

    def clean(self):
        """
        Check stock availability (if Product is provided).
        """
        cleaned = super().clean()
        product = cleaned.get('product')
        qty = cleaned.get('quantity')

        if product and qty is not None:
            if product.stock is not None and qty > product.stock:
                raise ValidationError(f"Not enough stock for {product.name}. Available: {product.stock}.")
        return cleaned

TransactionItemFormSet = inlineformset_factory(
    Transaction,
    TransactionItem,
    form=TransactionItemForm,
    extra=1,
    can_delete=True
)
