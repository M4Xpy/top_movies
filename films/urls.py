from django.urls import path

from .views import (
    index,
    CustomerCreateView,
    CustomerDeleteView,
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

]

app_name = "films"
