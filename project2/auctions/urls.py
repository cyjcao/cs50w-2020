from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("categories", views.categories, name="categories"),
    path("category/<int:category_id>", views.category, name="category"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("new_listing", views.create_listing, name="create"),
    path("listing/<int:listing_id>/add_comment", views.add_comment, name="add_comment"),
    path("listing/<int:listing_id>", views.listing, name="listing")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
