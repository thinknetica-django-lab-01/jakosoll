from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
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
    path('accounts/login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
]
