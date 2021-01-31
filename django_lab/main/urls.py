from django.urls import path
from .views import index, ProductListView, ProductDetailView, UpdateAccountView

urlpatterns = [
    path('', index, name='main_page'),
    path('goods/', ProductListView.as_view(), name='goods'),
    path('goods/<int:pk>', ProductDetailView.as_view(), name='goods_detail'),
    path('accounts/profile/', UpdateAccountView.as_view(), name='update_account'),
]
