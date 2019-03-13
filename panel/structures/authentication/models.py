import uuid
from django.db import models
from django.db.models.signals import pre_save
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
        user = self.model(phone_number=phone_number, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone_number, email=None, password=None, **extra_fields):
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
    id62 = models.CharField(max_length=100, db_index=True, blank=True, null=True)
    phone_number = models.CharField(unique=True, max_length=20,
    	help_text=_('Required. 20 characters or fewer. digits only.'),
	)

    full_name = models.CharField(_('full name'), max_length=150, blank=True)
    nick_name = models.CharField(_('nick name'), max_length=150, blank=True)
    email = models.EmailField(_('email address'), blank=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
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
            kwargs['force_insert'] =  False
            instance = super(AbstractUser, self).save(*args, **kwargs)
        return instance


class User(AbstractUser):
    """
    Users within the Django authentication system are represented by this
    model.

    Username and password are required. Other fields are optional.
    """

    def __str__(self):
        return self.nick_name

    def get_profile(self):
        from core.structures.account.models import Profile
        return Profile.objects.filter(created_by=self).first()

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
        unique_together = ('phone_number', 'nick_name')


class RegisterToken(models.Model):
    phone_number = models.CharField(unique=True, max_length=20,
    	help_text=_('Required. 20 characters or fewer. digits only.'),
	)
    token = models.CharField(_('token'), max_length=150, blank=True)

    class Meta:
        verbose_name = _('register token')
        verbose_name_plural = _('register tokens')


def send_verification_email(email, user):
    from ...libs.email import send_mail
    from django.conf import settings

    subject_template_name = "email/email_verify.txt"
    html_email_template_name = "email/email_verify.html"
    email_template_name = html_email_template_name
    code = str(uuid.uuid4())
    context = {
        "url" : getattr(settings, 'BASE_URL')+"/email_verify?c="+code,
        "name" : user.full_name
    }

    send_mail(
        subject_template_name,
        email_template_name,
        html_email_template_name,
        context,
        email, cc=getattr(settings, "MAIL_NOTIFICATION_CC", [])
    )

@receiver(pre_save, sender=User)
def verify_email(sender, instance, **kwargs):
    from django.conf import settings

    if getattr(settings, 'EMAIL_HOST') and getattr(settings, 'FROM_EMAIL'):
        email = instance.email
        existed_user = User.objects.filter(id=instance.id).first()
        if not existed_user:
            send_verification_email(email, instance)