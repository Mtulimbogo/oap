from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
# from django.conf.urls import url
from django.urls import include, path
from django.views import defaults as default_views
from django.views.generic import TemplateView
from portal.cv_registration import urls as cv_reg_urls
from portal.ega_org import urls as ega_reg_urls
from portal.university_regulator import urls as university_regulator_urls
# from django.contrib.auth.views import LoginView
# from portal.users.views import login_spana
# from portal.users import views
urlpatterns = [
    path("", TemplateView.as_view(template_name="pages/home.html"), name="home"),
    # path("", include(views.log), name="login_spana"),
    # url("", login_spana, name="l"),
    # path("", LoginView.as_view(
    #     template_name='account/login.html')),
    path(
        "about/", TemplateView.as_view(template_name="pages/about.html"), name="about"
    ),
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),

    # User management
    path("users/", include("portal.users.urls", namespace="users")),
    path("accounts/", include("allauth.urls")),
    path("info_registration/", include(cv_reg_urls)),
    path('university/', include(university_regulator_urls)),
    path('ega/', include(ega_reg_urls)),

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
