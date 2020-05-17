from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),

    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),

    path('login/', auth_views.LoginView.as_view(template_name="store/login.html"), name="login"),
    path('logout/', auth_views.LogoutView.as_view(template_name="store/store.html"), name="logout"),
    path('register/', views.register, name="register"),
    path('profile/', views.profile, name="profile"),
    path('profile/edit/', views.edit_profile, name="edit_profile"),

    path('create_product/', views.createProduct, name="create_product"),
    path('edit_product/<int:pk>/', views.editProduct, name="edit_product"),
    path('delete_product/<int:pk>/', views.deleteProduct, name="delete_product"),
    path('category/<str:category_name>/', views.show_products, name="category"),

    path('search/', views.search, name="search"),

]
