from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from .models import Product
from .forms import UpdateUserForm


def index(request):
    """Displays main page"""
    return render(request, 'index.html')


class ProductListView(ListView):
    """Displays product's list"""
    model = Product
    paginate_by = 10
    template_name = 'product_list.html'
    context_object_name = 'products'

    def get_queryset(self, **kwargs):
        tag = self.request.GET.get('tag')
        if tag:
            return Product.objects.filter(tags__name=tag)
        return super().get_queryset(**kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_name = self.request.GET.get('tag')
        if tag_name:
            tag = 'tag=' + tag_name
            context['tag'] = tag
        return context


class ProductDetailView(DetailView):
    """Displays product's detail view"""
    queryset = Product.objects.all()
    template_name = 'product_detail.html'
    context_object_name = 'product'


class UpdateAccountView(LoginRequiredMixin, UpdateView):
    """Displays user's account profile form"""
    form_class = UpdateUserForm
    login_url = '/'
    template_name = 'login_update.html'
    success_url = '/'

    def get_object(self, queryset=None):
        return User.objects.get(pk=self.request.user.id)

