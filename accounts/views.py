import smtplib

from rest_framework import generics
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.reverse import reverse

from accounts.models import Client, Manager
from accounts.serializers import ClientSerializer, \
    ClientRegistrationSerializer, InactiveProfileSerializer
from finapp import settings
from profiles.models import Profile
from .permissions import IsManagerPermission


class ClientsRegistration(generics.CreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientRegistrationSerializer

    def perform_create(self, serializer):
        manager_id = self.request.POST.get('manager')
        manager = Manager.objects.get(id=manager_id)
        if serializer.is_valid():
            try:
                server = smtplib.SMTP(settings.SMTP_server, 587)
                server.starttls()
                server.login(settings.DEFAULT_FROM_EMAIL,
                             settings.EMAIL_PASSWORD)
                msg = "Please follow this link to activate client's account " \
                      "http://127.0.0.1:8000/accounts/clients/"
                server.sendmail(settings.DEFAULT_FROM_EMAIL,
                                manager.user.email, msg)
                server.quit()
            except smtplib.SMTPException:
                print("Error: unable to send email")
        serializer.save()


class InactiveClients(viewsets.ModelViewSet):
    queryset = Client.objects.filter(is_active=False)
    serializer_class = ClientSerializer
    permission_classes = (IsAuthenticated, IsManagerPermission, )

    def perform_update(self, serializer):
        client = self.get_object()
        is_active = self.request.POST.get('is_active')
        if is_active and serializer.is_valid():
            try:
                server = smtplib.SMTP(settings.SMTP_server, 587)
                server.starttls()
                server.login(settings.DEFAULT_FROM_EMAIL,
                             settings.EMAIL_PASSWORD)
                msg = "Please follow this link to register profile " \
                      "http://127.0.0.1:8000%s" % reverse(
                        'profiles:profile_registration')
                server.sendmail(settings.DEFAULT_FROM_EMAIL,
                                client.user.email, msg)
                server.quit()
            except smtplib.SMTPException:
                print("Error: unable to send email")
        serializer.save()


class InactiveProfiles(viewsets.ModelViewSet):
    queryset = Profile.objects.filter(is_active=False)
    serializer_class = InactiveProfileSerializer
    permission_classes = (IsAuthenticated, IsManagerPermission, )
