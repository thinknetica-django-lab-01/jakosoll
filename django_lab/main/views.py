from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Product


def index(request):
    """Displays main page"""
    return render(request, 'index.html')


class ProductListView(ListView):
    """Displays product's list"""
    model = Product
    paginate_by = 10
    template_name = 'product_list.html'
    context_object_name = 'products'


class ProductDetailView(DetailView):
    """Displays product's detail view"""
    queryset = Product.objects.all()
    template_name = 'product_detail.html'
    context_object_name = 'product'
