from django.urls import path, include
from .views import index, ProductListView, \
    ProductDetailView, ProductAddView, \
    UpdateAccountView, ProductEditView, \
    subscription, ProductSearchView

urlpatterns = [
    path('', index, name='main_page'),
    path('goods/', ProductListView.as_view(), name='goods'),
    path('goods/<int:pk>/', ProductDetailView.as_view(), name='goods_detail'),
    path('goods/add/', ProductAddView.as_view(), name='goods_add'),
    path('goods/<int:pk>/edit/', ProductEditView.as_view(), name='goods_edit'),
    path('goods/search/', ProductSearchView.as_view(), name='search'),
    path('accounts/', include('allauth.urls')),
    path('accounts/profile/', UpdateAccountView.as_view(), name='update_account'),
    path('subscriptions/goods/', subscription, name='goods_subscriptions')
]
