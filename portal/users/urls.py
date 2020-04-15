from django.urls import path

from portal.users.views import (
    user_detail_view,
    user_redirect_view,
    user_update_view,
    user_redirect_to_page,
)

app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<str:username>/", view=user_detail_view, name="detail"),
    path("loginredirect/<str:applicant_group>/", view=user_redirect_to_page, name="user_redirect_to_page"),
]
