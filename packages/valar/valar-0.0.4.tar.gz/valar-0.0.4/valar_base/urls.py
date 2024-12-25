from django.urls import path

from views import search

urlpatterns = [

    path("get/<int:_id>", search.get),
]
