from django.urls import path
from .views import index, ProductListView, \
    ProductDetailView, ProductAddView, \
    UpdateAccountView, ProductEditView

urlpatterns = [
    path('', index, name='main_page'),
    path('goods/', ProductListView.as_view(), name='goods'),
    path('goods/<int:pk>/', ProductDetailView.as_view(), name='goods_detail'),
    path('goods/add/', ProductAddView.as_view(), name='goods_add'),
    path('goods/<int:pk>/edit/', ProductEditView.as_view(), name='goods_edit'),
    path('accounts/profile/', UpdateAccountView.as_view(), name='update_account'),
]
