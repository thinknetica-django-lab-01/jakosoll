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


def index(request: HttpRequest) -> HttpResponse:
    """Displays main page"""
    return render(request, 'index.html')


class ProductListView(ListView):
    """Displays product's list"""
    model = Product
    paginate_by: int = 10
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


# @method_decorator(cache_page(60 * 5), name='dispatch')
class ProductDetailView(DetailView):
    """Displays product's detail view"""
    queryset = Product.objects.all()
    template_name = 'product_detail.html'
    context_object_name = 'product'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.view_counter += 1
        self.object.save()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data()
        cache_product_id = 'cache_product_id:' + str(self.object.id)
        counter = cache.get(cache_product_id)
        if not counter:
            counter = self.object.view_counter
            cache.set(cache_product_id, counter, 60)
        context['counter'] = counter
        return context


class ProductAddView(PermissionRequiredMixin, CreateView):
    """Displays form for add product"""
    permission_required = 'main.add_product'
    model = Product
    form_class = ProductAddForm
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


class ProductEditView(PermissionRequiredMixin, UserPassesTestMixin, UpdateView):
    """Displays product edit form"""
    permission_required = 'main.change_product'
    form_class = ProductAddForm
    template_name = 'product_update.html'
    model = Product

    def test_func(self):
        return self.request.user.id == self.get_object().vendor_id


class UpdateAccountView(LoginRequiredMixin, UpdateView):
    """Displays user's account profile form"""
    form_class = UpdateUserForm
    template_name = 'login_update.html'
    success_url = '/'

    def get_object(self, queryset=None):
        return self.request.user


@login_required
def subscription(request: HttpRequest) -> HttpResponse:
    """Handles subscribe button"""
    if request.POST:
        form = forms.Form(request.POST or None)
        user = request.user
        if form.is_valid():
            subscriber, created = ProductSubscriber.objects.get_or_create(user=user)
            if created:
                messages.add_message(request, messages.SUCCESS, 'Вы подписались на рассылку')
            else:
                messages.add_message(request, messages.ERROR, 'Вы уже подписаны на рассылку')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        return HttpResponseBadRequest()
