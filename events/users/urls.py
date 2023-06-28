from django.urls import path

from events.users.views import (
    user_detail_view,
    user_redirect_view,
    user_update_view,
)
from events.users.views_emails import EmailsView

app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<int:pk>/", view=user_detail_view, name="detail"),
    path("emails/", view=EmailsView.as_view(), name="emails"),
]
