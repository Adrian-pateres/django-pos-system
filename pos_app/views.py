from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product, Transaction, TransactionItem
from .forms import ProductForm, TransactionForm, TransactionItemFormSet

@login_required
def product_list(request):
    products = Product.objects.all()
    return render(request, 'pos_app/product_list.html', {'products': products})

@login_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'pos_app/product_form.html', {'form': form})

@login_required
def transaction_create(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        formset = TransactionItemFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            transaction = form.save(commit=False)
            transaction.save()
            items = formset.save(commit=False)
            for item in items:
                item.transaction = transaction
                item.save()
            return redirect('transaction_detail', pk=transaction.pk)
    else:
        form = TransactionForm()
        formset = TransactionItemFormSet()
    return render(request, 'pos_app/transaction_form.html', {'form': form, 'formset': formset})

@login_required
def transaction_detail(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    items = TransactionItem.objects.filter(transaction=transaction)
    return render(request, 'pos_app/transaction_detail.html', {'transaction': transaction, 'items': items})