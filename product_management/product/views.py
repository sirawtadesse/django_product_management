from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View, CreateView, UpdateView, DeleteView
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserRegisterForm, ProductItemForm
from .models import ProductItem
from product_management.settings import LOW_QUANTITY
from django.contrib import messages

class Index(TemplateView):
    template_name='product/index.html'
    
class Dashboard(LoginRequiredMixin, View):
    def get(self, request):
        items = ProductItem.objects.filter(user=self.request.user.id).order_by('id')

        low_product = ProductItem.objects.filter(
            user=self.request.user.id,
            quantity_in_stock__lte=LOW_QUANTITY
        )

        out_of_stock_items = ProductItem.objects.filter(
            user=self.request.user.id,
            quantity_in_stock=0
        )

        if low_product.exists():
            if low_product.count() > 1:
                messages.error(request, f'{low_product.count()} items have low product')
            else:
                messages.error(request, f'{low_product.count()} item has low product in stock')

        if out_of_stock_items.exists():
            if out_of_stock_items.count() > 1:
                messages.error(request, f'{out_of_stock_items.count()} items are out of stock')
            else:
                messages.error(request, f'{out_of_stock_items.count()} item is out of stock')

        low_product_ids = low_product.values_list('id', flat=True)

        return render(request, 'product/dashboard.html', {'items': items, 'low_product_ids': low_product_ids})
    
class SignUpView(View):
    def get(self, request):
        form=UserRegisterForm()
        return render(request, 'product/signup.html', {'form':form})

    def post(self, request): 
        form=UserRegisterForm(request.POST)

        if form.is_valid():
            form.save()
            user= authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1']
            )

            login(request, user)
            return redirect('index')
        
        return render(request, 'product/signup.html', {'form':form}) 

class AddItem( LoginRequiredMixin ,CreateView):
     model=ProductItem
     form_class=ProductItemForm
     template_name='product/item_form.html'
     success_url=reverse_lazy('dashboard')

     def get_context_data(self, **kwargs):
          context=super().get_context_data()
          return context
     
     def form_valid(self, form):
          form.instance.user=self.request.user
          return super().form_valid(form)


class EditItem( LoginRequiredMixin ,UpdateView):
     model=ProductItem
     form_class=ProductItemForm
     template_name='product/item_form.html'
     success_url=reverse_lazy('dashboard')          


class DeleteItem( LoginRequiredMixin ,DeleteView):
     model=ProductItem
     template_name='product/delete_item.html'
     success_url=reverse_lazy('dashboard')     
     context_object_name='item'