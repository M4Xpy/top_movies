from django.urls import path

from .views import (
    index,
    CustomerCreateView,
    CustomerDeleteView,

    ActorCreateView,
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

]

app_name = "films"
