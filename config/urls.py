from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views import defaults as default_views
from django.views.generic import TemplateView

from events.users.forms import UserSignupForm


class HomePageView(TemplateView):
    template_name = "pages/home.html"
    signup = UserSignupForm()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context["events"] = Event.objects.all()  # Or apply any filter/query based on your requirements
        context["form"] = UserSignupForm()

        if not self.request.user.is_authenticated:
            pass
        elif self.request.method == "POST":
            pass
        # return render(self.request, "account/short_signup_form.html", context=context)
        return context


urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("about/", TemplateView.as_view(template_name="pages/about.html"), name="about"),
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    # User management
    path("users/", include("events.users.urls", namespace="users")),
    path("accounts/", include("allauth.urls")),
    path("", include("apps.event.urls")),
    path("", include("apps.membership.urls")),
    path("", include("apps.usac.urls")),
    # Your stuff: custom urls includes go here
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
