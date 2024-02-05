from django.urls import path

from .views import (
    index,
    CustomerCreateView,
    CustomerDeleteView,

    ActorCreateView,
    ActorListView,
    ActorUpdateView,
    ActorDeleteView,

    CountryCreateView,
    CountryListView,
    CountryUpdateView,
    CountryDeleteView,

    GenreCreateView,
    GenreListView,
    GenreUpdateView,
    GenreDeleteView,
)

urlpatterns = [
    path("",
         index,
         name="index", ),
    path("customers/create/",
         CustomerCreateView.as_view(),
         name="customer-create", ),
    path("customers/<int:pk>/delete/",
         CustomerDeleteView.as_view(),
         name="customer-delete", ),
    # Actor  CRUD
    path("actors/create/",
         ActorCreateView.as_view(),
         name="actor-create", ),
    path("actors/",
         ActorListView.as_view(),
         name="actor-list", ),
    path("actors/<int:pk>/update/",
         ActorUpdateView.as_view(),
         name="actor-update", ),
    path("actors/<int:pk>/delete/",
         ActorDeleteView.as_view(),
         name="actor-delete", ),
    # Country  CRUD
    path("countries/create/",
         CountryCreateView.as_view(),
         name="country-create", ),
    path("countries/",
         CountryListView.as_view(),
         name="country-list", ),
    path("countries/<int:pk>/update/",
         CountryUpdateView.as_view(),
         name="country-update", ),
    path("countries/<int:pk>/delete/",
         CountryDeleteView.as_view(),
         name="country-delete", ),
    # Genre  CRUD
    path("genres/create/",
         GenreCreateView.as_view(),
         name="genre-create", ),
    path("genres/",
         GenreListView.as_view(),
         name="genre-list", ),
    path("genres/<int:pk>/update/",
         GenreUpdateView.as_view(),
         name="genre-update", ),
    path("genres/<int:pk>/delete/",
         GenreDeleteView.as_view(),
         name="genre-delete", ),

]

app_name = "films"
