from django.conf.urls import url
from rest_framework import routers
from accounts.views import ClientsRegistration, InactiveClients, \
    InactiveProfiles

router = routers.DefaultRouter()
router.register(r'clients', InactiveClients)
router.register(r'profiles', InactiveProfiles)

urlpatterns = [
    url(r'^client/register/$', ClientsRegistration.as_view(),
        name="register"),
]
urlpatterns += router.urls
