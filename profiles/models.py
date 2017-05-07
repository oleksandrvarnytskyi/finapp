from django.db import models
from django.utils.translation import ugettext as _

from accounts.models import Client


class Profile(models.Model):
    client = models.OneToOneField(
        Client,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name=_('Client')
    )
    balance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_('Balance'),
        help_text=_('amount of USD, for instance 10.55'),
        default='0.00'
    )
    pin_code = models.PositiveIntegerField(
        verbose_name=_('Pin code'),
        help_text=_('For instance XXXX where X is any number from 0 to 9'),
    )
    is_active = models.BooleanField(
        _('is active'),
        default=True,
        help_text=_(
            'Designates whether this profile should be treated as active. '),
    )

    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')

    def __unicode__(self):
        return '{} - {}'.format(self.client, self.balance)

    def save(self, *args, **kwargs):
        client_obj = Client.objects.get(id=self.client.id)
        if not client_obj.is_active:
            raise ValueError("Creating a profile isn't allowed yet!")
        super(Profile, self).save(*args, **kwargs)
