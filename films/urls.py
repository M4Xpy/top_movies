from django.urls import path

from .views import (
    index,
    CustomerCreateView,
    CustomerDeleteView,

    ActorCreateView,
    ActorListView,
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

]

app_name = "films"
