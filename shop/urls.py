from django.urls import path
from . import views

app_name = "shop"

urlpatterns = [
    path("", views.home, name="home"),
    path("products/", views.product_list, name="product_list"),
    path("products/category/<slug:category_slug>/", views.product_list, name="category"),
    path("product/<slug:slug>/", views.product_detail, name="product_detail"),
    path("cart/", views.cart_view, name="cart"),
    path("cart/add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/update/<int:item_id>/", views.update_cart, name="update_cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("orders/", views.order_list, name="orders"),
    path("order/<str:order_number>/", views.order_detail, name="order_detail"),
    path("order/<str:order_number>/cancel/", views.cancel_order, name="cancel_order"),
    path("signup/", views.signup_view, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.profile, name="profile"),
    path("address/add/", views.add_address, name="add_address"),
    path("address/<int:pk>/edit/", views.edit_address, name="edit_address"),
    path("address/<int:pk>/delete/", views.delete_address, name="delete_address"),
    path("wishlist/", views.wishlist_view, name="wishlist"),
    path("wishlist/<int:product_id>/", views.toggle_wishlist, name="toggle_wishlist"),
    path("review/<slug:slug>/", views.add_review, name="add_review"),
    path("newsletter/", views.newsletter_subscribe, name="newsletter"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("install/", views.install_app, name="install"),
    path("dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("dashboard/product/", views.admin_product_edit, name="admin_product_add"),
    path("dashboard/product/<int:pk>/", views.admin_product_edit, name="admin_product_edit"),
    path("api/search/", views.search_api, name="search_api"),
]
