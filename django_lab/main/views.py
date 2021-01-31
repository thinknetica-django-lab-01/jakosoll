from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from .models import Product, Category, Tag
from .forms import UpdateUserForm, ProductAddForm


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


class ProductAddView(PermissionRequiredMixin, CreateView):
    """Displays form for add product"""
    permission_required = 'main.add_product'
    model = Product
    form_class = ProductAddForm
    login_url = '/'
    template_name = 'product_add.html'

    def get_context_data(self, **kwargs):
        context = super(ProductAddView, self).get_context_data()
        context['category'] = Category.objects.all()
        context['tags'] = Tag.objects.all()
        return context

    def form_valid(self, form):
        product = form.save(commit=False)
        product.vendor_id = self.request.user.id
        product.save()
        return super(ProductAddView, self).form_valid(form)


class ProductEditView(PermissionRequiredMixin, UpdateView):
    """Displays product edit form"""
    permission_required = 'main.edit_product'
    form_class = ProductAddForm
    login_url = '/'
    template_name = 'product_update.html'
    model = Product


class UpdateAccountView(LoginRequiredMixin, UpdateView):
    """Displays user's account profile form"""
    form_class = UpdateUserForm
    login_url = '/'
    template_name = 'login_update.html'
    success_url = '/'

    def get_object(self, queryset=None):
        return self.request.user

