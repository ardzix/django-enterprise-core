'''
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# File: models.py
# Project: django-panel-core
# File Created: Tuesday, 25th February 2020 1:26:07 am
# 
# Author: Arif Dzikrullah
#         ardzix@hotmail.com>
#         https://github.com/ardzix/>
# 
# Last Modified: Tuesday, 25th February 2020 1:26:09 am
# Modified By: Arif Dzikrullah (ardzix@hotmail.com>)
# 
# Hand-crafted & Made with Love
# Copyright - 2018 Ardz Co, https://github.com/ardzix/django-panel-core
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''


import uuid
from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils import timezone
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from ...libs.base62 import base62_encode


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, phone_number, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not phone_number:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        # username = self.model.normalize_username(username)
        user = self.model(
            phone_number=phone_number,
            email=email,
            **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone_number, email=None,
                    password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(phone_number, email, password, **extra_fields)

    def create_superuser(self, phone_number, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(phone_number, email, password, **extra_fields)


class AbstractUser(AbstractBaseUser, PermissionsMixin):
    id62 = models.CharField(
        max_length=100,
        db_index=True,
        blank=True,
        null=True)
    phone_number = models.CharField(unique=True, max_length=20,
                                    help_text=_(
                                        'Required. 20 characters or fewer. digits only.'),
                                    )

    full_name = models.CharField(_('full name'), max_length=150, blank=True)
    nick_name = models.CharField(_('nick name'), max_length=150, blank=True)
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=False,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    is_sent_email = models.BooleanField(default=True)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        abstract = True

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        return self.full_name

    def get_short_name(self):
        """Return the short name for the user."""
        return self.nick_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def save(self, *args, **kwargs):
        instance = super(AbstractUser, self).save(*args, **kwargs)
        if self.id and not self.id62:
            self.id62 = base62_encode(self.id)
            kwargs['force_insert'] = False
            instance = super(AbstractUser, self).save(*args, **kwargs)
        return instance


class User(AbstractUser):
    """
    Users within the Django authentication system are represented by this
    model.

    Username and password are required. Other fields are optional.
    """

    def __str__(self):
        return '%s <%s>' % (self.full_name, self.email)

    def get_groups(self):
        return ', '.join(list(self.groups.values_list('name', flat=True)))

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
        unique_together = ('phone_number', 'full_name')


class RegisterToken(models.Model):
    phone_number = models.CharField(unique=True, max_length=20,
                                    help_text=_(
                                        'Required. 20 characters or fewer. digits only.'),
                                    )
    token = models.CharField(_('token'), max_length=150, blank=True)

    class Meta:
        verbose_name = _('register token')
        verbose_name_plural = _('register tokens')


class EmailVerification(models.Model):
    email = models.EmailField()
    code = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = _('Email Varification')
        verbose_name_plural = _('Email Varifications')


def send_verification_email(email, user, base_url=None, *args, **kwargs):
    from ...libs.email import send_mail
    from ...libs.otp import generate_otp_code
    from django.conf import settings

    subject_template_name = "email/email_verify.txt"
    html_email_template_name = "email/email_verify.html"
    email_template_name = html_email_template_name
    code = generate_otp_code(6)

    context = {
        "code": code,
        "name": user.full_name
    }

    send_mail(
        subject_template_name,
        email_template_name,
        html_email_template_name,
        context,
        email, cc=getattr(settings, "MAIL_NOTIFICATION_CC", [])
    )

    ev, created = EmailVerification.objects.get_or_create(
        email=email
    )
    ev.code = code
    ev.is_verified = False
    ev.save()

    return ev


@receiver(pre_save, sender=User)
def verify_email(sender, instance, **kwargs):
    from django.conf import settings

    if getattr(settings, 'AUTO_VERIFY_EMAIL', False):
        email = instance.email
        if instance.is_sent_email:
            existed_user = User.objects.filter(id=instance.id).first()
            if not existed_user:
                send_verification_email(
                    email,
                    instance,
                    is_reset_password=True
                )
            else:
                if email != existed_user.email:
                    send_verification_email(email, instance)


@receiver(post_save, sender=User)
def save_ev(sender, instance, **kwargs):
    if getattr(settings, 'AUTO_VERIFY_EMAIL', False):
        ev = EmailVerification.objects.filter(email=instance.email).last()
        if ev:
            ev.user = instance
            ev.save()
