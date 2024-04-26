from django.urls import path, include
from apps.users.views import UserAPIView

urlpatterns = [
    path('', UserAPIView.as_view({
        "get": "get",
        "post": "create",
        "patch": "update",
        "delete": "destroy"
    })),
]
