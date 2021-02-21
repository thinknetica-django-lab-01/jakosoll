from __future__ import annotations
from django.http import HttpResponseRedirect, HttpResponseBadRequest, HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, Category, Tag, ProductSubscriber
from .forms import UpdateUserForm, ProductAddForm
from django import forms
from django.core.cache import cache
from django.db.models.query import QuerySet
from typing import Optional, Union, Dict, Any
from django.contrib.auth.models import User, AnonymousUser


def index(request: HttpRequest) -> HttpResponse:
    """Displays main page"""
    return render(request, 'index.html')


class ProductListView(ListView):
    """Displays product's list"""
    model = Product
    paginate_by: int = 10
    template_name: str = 'product_list.html'
    context_object_name: str = 'products'

    def get_queryset(self, **kwargs) -> 'QuerySet[Product]':
        tag: Optional[str] = self.request.GET.get('tag')
        if tag:
            return Product.objects.filter(tags__name=tag)
        return super().get_queryset()

    def get_context_data(self, *, object_list=None, **kwargs) -> Dict[str, Any]:
        context: Dict[str, Any] = super().get_context_data(**kwargs)
        tag_name = self.request.GET.get('tag')
        if tag_name:
            tag = 'tag=' + tag_name
            context['tag'] = tag
        return context


# @method_decorator(cache_page(60 * 5), name='dispatch')
class ProductDetailView(DetailView):
    """Displays product's detail view"""
    queryset: QuerySet = Product.objects.all()
    template_name: str = 'product_detail.html'
    context_object_name: str = 'product'

    def get(self, request, *args, **kwargs) -> HttpResponse:
        self.object: Product = self.get_object()
        self.object.view_counter += 1
        self.object.save()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context: Dict[str, Any] = super(ProductDetailView, self).get_context_data()
        cache_product_id: str = 'cache_product_id:' + str(self.object.id)
        counter: int = cache.get(cache_product_id)
        if not counter:
            counter = self.object.view_counter
            cache.set(cache_product_id, counter, 60)
        context['counter'] = counter
        return context


class ProductAddView(PermissionRequiredMixin, CreateView):
    """Displays form for add product"""
    permission_required: str = 'main.add_product'
    model = Product
    form_class = ProductAddForm
    template_name: str = 'product_add.html'

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context: Dict[str, Any] = super(ProductAddView, self).get_context_data()
        context['category'] = Category.objects.all()
        context['tags'] = Tag.objects.all()
        return context

    def form_valid(self, form: forms.BaseModelForm) -> HttpResponse:
        product = form.save(commit=False)
        product.vendor_id = self.request.user.id
        product.save()
        return super(ProductAddView, self).form_valid(form)


class ProductEditView(PermissionRequiredMixin, UserPassesTestMixin, UpdateView):
    """Displays product edit form"""
    permission_required: str = 'main.change_product'
    form_class = ProductAddForm
    template_name: str = 'product_update.html'
    model = Product

    def test_func(self) -> bool:
        product: Product = self.get_object()
        return self.request.user.id == product.vendor_id


class UpdateAccountView(LoginRequiredMixin, UpdateView):
    """Displays user's account profile form"""
    form_class = UpdateUserForm
    template_name: str = 'login_update.html'
    success_url: str = '/'

    def get_object(self, queryset=None) -> Union[User, AnonymousUser]:
        return self.request.user


@login_required
def subscription(request: HttpRequest) -> Union[HttpResponseRedirect, HttpResponseBadRequest]:
    """Handles subscribe button"""
    if request.POST:
        form = forms.Form(request.POST or None)
        user: Union[User, AnonymousUser] = request.user
        if form.is_valid():
            subscriber, created = ProductSubscriber.objects.get_or_create(user=user)
            if created:
                messages.add_message(request, messages.SUCCESS, 'Вы подписались на рассылку')
            else:
                messages.add_message(request, messages.ERROR, 'Вы уже подписаны на рассылку')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return HttpResponseBadRequest()
