from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing/<int:listing_id>", views.listing_view, name="listing"),
    path("watchlist/<int:listing_id>", views.watchlist_toggle, name="watchlist_toggle"),
    path("close-auction/<int:listing_id>", views.close_auction, name="close_auction"),
    path("create/", views.create_listing_view, name="create_listing"),
    path("watchlist/", views.watchlist_view, name="my_watchlist"),
    path("add-comment/<int:listing_id>", views.add_comment, name="add_comment"),
    path("categories", views.category_list, name="category_list"),
    path("categories/<int:category_id>", views.listing_by_category, name="listing_by_category"),
]
