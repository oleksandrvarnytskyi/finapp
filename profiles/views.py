import smtplib

from django.shortcuts import redirect
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from finapp import settings
from profiles.models import Profile
from profiles.serializers import ProfileRegistrationSerializer, \
    ProfileDetailViewSerializer, ProfileLoginSerializer


class ProfileRegistration(generics.CreateAPIView):
    queryset = Profile.objects.filter(is_active=True)
    serializer_class = ProfileRegistrationSerializer
    permission_classes = (IsAuthenticated, )


class ProfileDetailView(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileDetailViewSerializer
    permission_classes = (IsAuthenticated,)

    def perform_update(self, serializer):
        profile = self.get_object()
        is_active = self.request.POST.get('is_active')
        if not is_active and serializer.is_valid():
            try:
                server = smtplib.SMTP(settings.SMTP_server, 587)
                server.starttls()
                server.login(settings.DEFAULT_FROM_EMAIL,
                             settings.EMAIL_PASSWORD)
                msg = "Please follow this link to delete profile " \
                      "http://127.0.0.1:8000/accounts/profiles/"
                server.sendmail(settings.DEFAULT_FROM_EMAIL,
                                profile.client.manager.user.email, msg)
                server.quit()
            except smtplib.SMTPException:
                print("Error: unable to send email")
        serializer.save()


class ProfileLogin(generics.CreateAPIView):
    queryset = Profile.objects.filter(is_active=True)
    serializer_class = ProfileLoginSerializer
    permission_classes = (IsAuthenticated, )

    def post(self, request, *args, **kwargs):
        client = request.POST.get('client')
        pin_code = int(request.POST.get('pin_code'))
        profile = Profile.objects.get(client=client)
        if pin_code == profile.pin_code:
            return redirect('profiles:profile_detail', profile.pk)
        else:
            return redirect('profiles:profile_login')
