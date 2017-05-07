from django.contrib.auth.validators import UnicodeUsernameValidator, \
    ASCIIUsernameValidator
from django.core import validators
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import six
from django.utils.translation import ugettext as _

from finapp import settings


class User(AbstractUser):
    username_validator = UnicodeUsernameValidator() if six.PY3 else \
        ASCIIUsernameValidator()
    username = models.CharField(
        _('username'),
        max_length=150,
        blank=True,
        help_text=_(
            'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    email = models.EmailField(
        _('Email'),
        unique=True,
        db_index=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    @property
    def is_manager(self):
        try:
            if self.manager:
                return True
        except:
            return False

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __unicode__(self):
        return self.email


class Manager(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='manager',
        verbose_name=_('Manager'),
        null=True, blank=True,
    )

    class Meta:
        verbose_name = _('Manager')
        verbose_name_plural = _('Managers')

    def __str__(self):
        return self.user.email


class PassportNumberValidator(validators.RegexValidator):
    regex = r'^\w{2} \d{6}$'
    message = _(
        'Enter a passport number in the format: LL XXXXXX only.'
        'Where L is any letter and X is any number from 0 to 9'
    )


class Client(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='client',
        verbose_name=_('Client')
    )
    manager = models.ForeignKey(
        Manager,
        related_name='clients',
        verbose_name=_('Manager')
    )
    passport_number_validator = PassportNumberValidator()

    passport_number = models.CharField(
        _('passport number'),
        max_length=10,
        unique=True,
        help_text=_(
            'Required a passport number in the format: LL XXXXXX only.'
            'Where L is any letter and X is any number from 0 to 9'
        ),
        validators=[passport_number_validator],
        error_messages={
            'unique': _("A client with this passport number already exists."),
        },
    )
    is_active = models.BooleanField(
        _('is active'),
        default=False,
        help_text=_(
            'Designates whether this client should be treated as active. '
        ),
    )

    class Meta:
        verbose_name = _('Client')
        verbose_name_plural = _('Clients')

    def __str__(self):
        return self.user.email
