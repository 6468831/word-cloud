from django.urls import path
from .views import ShowCloud


urlpatterns = [
    path("", ShowCloud.as_view(), name="show-cloud")
]

