from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("categories/", views.CategoryView.as_view(), name="categories"),
    path("categories/<int:category_id>/", views.CategoryDetailView.as_view(), name="category-detail"),
    path("states/", views.StateView.as_view(), name="states"),
    path("incidents/", views.IncidentView.as_view(), name="incidents"),
]