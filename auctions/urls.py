from django.urls import path

from . import views

#app_name = "auctions"

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="create_listing"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("listing/close/<int:id>", views.close_listing, name="close_listing"),
    path("watchlist/remove/<int:id>", views.remove_watchlist, name="remove_watchlist"),
    path("watchlist/add/<int:id>", views.add_watchlist, name="add_watchlist"),
    path("listing/<int:id>/comments", views.comments, name="comments"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.categories, name="categories"),
    path("category/<str:category>", views.category, name="category"),
]
