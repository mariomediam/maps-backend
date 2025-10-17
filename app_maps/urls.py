from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("categories/", views.CategoryView.as_view(), name="categories"),
    path("categories/<int:category_id>/", views.CategoryDetailView.as_view(), name="category-detail"),
    path("states/", views.StateView.as_view(), name="states"),
    path("incidents/", views.IncidentView.as_view(), name="incidents"),
    path("incidents/photography/<int:id_photography>/", views.PhotographyView.as_view(), name="photographies"),
    path("incidents/<int:id_incident>/", views.IncidentDetailView.as_view(), name="incident-detail"),
    path("incidents/miniature/<int:id_incident>", views.PhotographyMiniatureView.as_view(), name="photography-miniature"),
    path("priorities/", views.PriorityView.as_view(), name="priorities"),
    path("closure-types/", views.ClosureTypeView.as_view(), name="closure-types"),
]