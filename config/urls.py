from datetime import date

from allauth.account.views import SignupView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.core.mail import send_mail
from django.db.models import Q
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import include, path
from django.views import defaults as default_views
from django.views.generic import TemplateView

from apps.event.models import Event
from events.users.forms import UserSignupForm


class HomePageView(TemplateView):
    """This view loads if the user is logged in"""

    template_name = "pages/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #  Feature event
        context["featured_events"] = Event.objects.all().filter(
            Q(logo__isnull=False) & ~Q(logo="") & Q(featured_event=True) & Q(end_date__gte=date.today())
        )[:6]
        # print(f"featured list: {[(i.name, i.logo) for i in context['featured_events']]}")
        return context


class HomePageSignUpView(SignupView):
    """This view loads if you are not logged in"""

    template_name = "pages/home.html"  # your custom template
    form_class = UserSignupForm  # your custom form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #  Feature event
        context["featured_events"] = Event.objects.all().filter(
            Q(logo__isnull=False) & ~Q(logo="") & Q(featured_event=True) & Q(end_date__gte=date.today())
        )[:6]
        # print(f"featured list: {[(i.name, i.logo) for i in context['featured_events']]}")
        return context

    def form_valid(self, form):
        # Here we can add our custom logic for login
        parent_email = form.cleaned_data.get("parent_email")
        parent_name = form.cleaned_data.get("parent_name")
        render_to_string(
            "emails/new_account_parent_notifcation.html",
            {
                "parent_name": parent_name,
            },
        )
        if parent_email:
            send_mail(
                "Your child has created an account at Bicycle Colorado"
                f"Hello {parent_name},\n\nYour child has created an account at Bicycle Colorado\n "
                f"https://events.bicyclecolorado.org",
                "
            send_mail(
                "Your child has created an account at Bicycle Colorado"
                f"Hello {parent_name},\n\nYour child has created an account at Bicycle Colorado\n "
                f"https://events.bicyclecolorado.org",
                "info@bicyclecolorado.org",
                [parent_email],
                fail_silently=False,
            )
        # Don't forget to call super
        return super().form_valid(form)

    def form_invalid(self, form):
        # Here you can handle the form errors
        return render(self.request, self.template_name, {"form": form})


if "events.bicycecolorado.org" in settings.ALLOWED_HOSTS:
    robots = "prod_robots.txt"
else:
    robots = "dev_robots.txt"

urlpatterns = [
    path("", HomePageSignUpView.as_view(), name="home"),
    path("home", HomePageView.as_view(), name="homepage"),
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    # User management
    path("users/", include("events.users.urls", namespace="users")),
    # Accounts
    path("accounts/", include("allauth.urls")),
    # Apps
    path("", include("apps.event.urls")),
    path("", include("apps.membership.urls")),
    path("", include("apps.usac.urls")),
    path("", include("apps.store.urls")),
    # Your stuff: custom urls includes go here
    path(
        "robots.txt",
        TemplateView.as_view(template_name=robots, content_type="text/plain"),
        name="robots",
    ),
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
