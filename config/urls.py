from allauth.account.views import SignupView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.core.mail import send_mail
from django.urls import include, path
from django.views import defaults as default_views
from django.views.generic import TemplateView
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from allauth.account.adapter import get_adapter
from allauth.account.utils import complete_signup
from allauth.exceptions import ImmediateHttpResponse
from events.users.forms import UserSignupForm
from django.contrib import messages


class HomePageView(SignupView):
    template_name = 'pages/home.html'  # your custom template
    form_class = UserSignupForm  # your custom form

    def form_valid(self, form):
        # Here we can add our custom logic for login
        parent_email = form.cleaned_data.get('parent_email')
        parent_name = form.cleaned_data.get('parent_name')

        send_mail(
            'Login Notification for Your Child',
            f'Hello {parent_name},\n\nYour child has logged into their account in events.',
            'from@example.com',
            [parent_email],
            fail_silently=False,
        )
        # Don't forget to call super
        return super().form_valid(form)

    def form_invalid(self, form):
        # Here you can handle the form errors
        return render(self.request, self.template_name, {'form': form})


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
