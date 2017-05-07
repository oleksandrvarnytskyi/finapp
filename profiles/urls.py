from django.conf.urls import url

from profiles.views import ProfileRegistration, ProfileDetailView, ProfileLogin

urlpatterns = [
    url(r'^registration/$', ProfileRegistration.as_view(),
        name="profile_registration"),
    url(r'^detail/(?P<pk>\d+)/$', ProfileDetailView.as_view(),
        name="profile_detail"),
    url(r'^login/$', ProfileLogin.as_view(),
        name="profile_login"),
]
