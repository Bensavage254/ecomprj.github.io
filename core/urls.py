from django.urls import path
from core.views import add_to_cart, add_to_wishlist, ajax_add_review, cart_view, category_list_view, category_product_list_view, checkout_view, delete_item_from_cart, filter_product, index, product_detail_view, product_list_view, search_views, tag_list, update_cart, vendor_detail_view, vendor_list_view, Wishlist_model, wishlist_view,payment_failed_view
from . import views


app_name ="core"

urlpatterns = [
    #Homepage
    path("", index, name="index"),
    path("products/", product_list_view, name="product-list"),
    path("product/<pid>/", product_detail_view, name="product-detail"),

    #categories
    path("category/", category_list_view, name="category-list"),
    path("category/<cid>/", category_product_list_view, name="category-product-list"),

    #vendors
    path("vendors/", vendor_list_view, name="vendor-list"),
    path("vendor/<vid>/", vendor_detail_view, name="vendor-detail"),

    #tags
    path("products/tag/<slug:tag_slug>/", tag_list, name="tags"),

    #Add reviews
    path("ajax-add-review/<int:pid>/", ajax_add_review, name="ajax-add-review"),

    #Search
    path("search/", search_views, name="search"),

    #Filter
    path("filter-products/", filter_product, name="filter-product"),

    #Cart
    path("add-to-cart/", add_to_cart, name="add-to-cart"),

    #cart page url
    path("cart/", cart_view, name="cart"),

    #delete item from cart
    path("delete-from-cart/", delete_item_from_cart, name="delete-from-cart"),

    #update item from cart
    path("update-cart/", update_cart, name="update-cart"),

    #checkout 
    path("checkout/", checkout_view, name="checkout"),

    #payment successfull
    #path("payment-completed/",payment_completed_view, name="payment-completed"),

    #payment failed
    path("payment-failed/",payment_failed_view, name="payment-failed"),

    #mpesapayment
    path('payment/',views.payment_view, name='payment'),

    #wishlistpage
    path('wishlist/',wishlist_view, name='wishlist'),

    #add-to-wishlist
    path("add-to-wishlist/",add_to_wishlist, name="add-to-wishlist"),

    #mpesaurl
    path('mpesaapi/', views.mpesaapi, name='mpesaapi'),
]