from django import forms
from django.forms import inlineformset_factory
from django.core.exceptions import ValidationError
from .models import Product, Transaction, TransactionItem

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'stock']

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['teller']

class TransactionItemForm(forms.ModelForm):
    class Meta:
        model = TransactionItem
        fields = ['product', 'quantity']

    def clean_quantity(self):
        qty = self.cleaned_data.get('quantity')
        if qty is None or qty <= 0:
            raise ValidationError("Quantity must be a positive number.")
        return qty

    def clean(self):
        cleaned = super().clean()
        product = cleaned.get('product')
        qty = cleaned.get('quantity')
        if product and qty and qty > product.stock:
            raise ValidationError(f"Not enough stock for {product.name}. Available: {product.stock}.")
        return cleaned

TransactionItemFormSet = inlineformset_factory(
    Transaction,
    TransactionItem,
    form=TransactionItemForm,
    extra=1,
    can_delete=True
)