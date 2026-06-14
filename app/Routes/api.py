from django.urls import include, path


urlpatterns = [
    path("user/v1/", include("app.Routes.user.v1")),
    path("admin/v1/", include("app.Routes.admin.v1")),
]
