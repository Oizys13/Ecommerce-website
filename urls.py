from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy


urlpatterns = [
    path('password/', auth_views.PasswordChangeView.as_view(success_url=reverse_lazy('Home'), template_name='base/password.html'), name='password'),
    path('register/', views.register, name = 'register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('myaccount/<str:pk>', views.profile, name='myaccount'),
    path('', views.home, name='Home'),
    path('search/', views.search, name='shop'),
    path('cart/<int:id>', views.cart_add, name='cart'),
    path('myaccount/cart/', views.cart_list, name='cart_list'),
    path('wishlist/<int:id>', views.wishlist_add, name='wishlist'),
    path('myaccount/wishlist/', views.wish_list, name='wish_list'),
    path('product/<str:pk>', views.product, name="product"),
    path('sell/', views.Sell, name= "sell"),
    path('edit/<str:pk>/', views.editProduct, name= "edit"),
    path('delete/<str:pk>', views.delete_product, name='delete'),
    path('products/man/', views.man, name="man"),
    path('products/woman/', views.woman, name="woman"),
    path('products/kids/', views.kids, name="kids"),
    path('contact1/', views.contact1, name="contact1"),
    path('form/', views.form, name="form"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('profile/<str:pk>', views.admin_profile, name='profile'),
    path('profile/<str:pk>/admin-panel', views.admin_page, name='admin_page'),
    path('form/', views.show_form, name='form'),
    path('CreatePDF/',views.pdf_report_creat,name='createpdf'),
    path('about/',views.us,name='about'),
]