import datetime, uuid, operator

from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import get_user_model, authenticate, password_validation
from django.db.models import Q

from rest_framework import exceptions
from rest_framework.authtoken.models import Token
from social_django.utils import load_strategy, load_backend

from phonenumbers import (
    parse as phone_number_parse,
    is_possible_number,
    is_valid_number,
)
from phonenumbers.phonenumberutil import NumberParseException

from core.libs import exceptions as custom_exceptions
from enterprise.libs.otp import OTPManager, generate_otp_code
from enterprise.structures.authentication.models import (
    PhoneVerification,
    EmailVerification,
)


"""
# environment variable to customize and dynamicly settings
# - USE_TOKEN_EXPIRED (boolean): validate DRF token expiry
# - EXPIRED_TOKEN_TIMEDELTA (python timedelta): time expired in timedelta. eg: timedelta(hours=72)
# - OAUTH_REDIRECT_URI (string): Oauth will be redirected
# - AUTH_USERNAME_FIELD (string): method authenticate() use USERNAME_FIELD, so provide that field to settings. 
#        default is phone_number
# - USE_VERIFY_EXPIRED (boolean): validate OTP/hash code is valid and not expired
# - VERIFY_USER_METHODS (list): activate user using email and/or phone_number. default ["email"]
# - VERIFY_EXPIRED_TIMEDELTA (python timedelta): time expired in timedelta. eg: timedelta(hours=1) 
# - EMAIL_VERIFY_BASE_URL (string): URL backend verification (to check/verify OTP code/hash)
# - SMS_GATEWAY_PROVIDER (string): SMS gateway provider. available providers: wavecell, nexmo. default wavecell
# - OTP_BRAND (string): SMS Masking. eg: Enterprise OTP
# - OTP_TEMPLATE (string): Template OTP.
# - OTP_CODE_LENGTH (integer): Length of OTP code. eg 6. default 4
"""
USE_TOKEN_EXPIRED = getattr(settings, "USE_TOKEN_EXPIRED", False)
EXPIRED_TOKEN_TIMEDELTA = getattr(
    settings, "EXPIRED_TOKEN_TIMEDELTA", datetime.timedelta(hours=72)
)
OAUTH_REDIRECT_URI = getattr(settings, "OAUTH_REDIRECT_URI", "/authentication/oauth/")
AUTH_USERNAME_FIELD = getattr(settings, "AUTH_USERNAME_FIELD", "phone_number")

# user verification
USE_VERIFY_EXPIRED = getattr(settings, "USE_VERIFY_EXPIRED", False)
VERIFY_USER_METHODS = getattr(settings, "VERIFY_USER_METHODS", ["email"])
VERIFY_EXPIRED_TIMEDELTA = getattr(
    settings, "VERIFY_EXPIRED_TIMEDELTA", datetime.timedelta(hours=1)
)
EMAIL_VERIFY_BASE_URL = getattr(
    settings, "EMAIL_VERIFY_BASE_URL", "http://localhost:8000/"
)

# OTP Manager
SMS_GATEWAY_PROVIDER = getattr(settings, "SMS_GATEWAY_PROVIDER", "wavecell")
OTP_BRAND = getattr(settings, "OTP_BRAND", "Django OTP")
OTP_TEMPLATE = getattr(
    settings,
    "OTP_TEMPLATE",
    "Kode verifikasi Anda (OTP): {code}. JANGAN MEMBERITAHU KODE RAHASIA INI KE SIAPAPUN termasuk pihak WeCare.id. Waspada penipuan!",
)
OTP_CODE_LENGTH = getattr(settings, "OTP_CODE_LENGTH", 4)


class AuthenticationManager(object):
    def _time_is_valid(self, value_to_check, relate, value_comparation):
        return relate(value_to_check, value_comparation)

    def _get_user(self, field_name, value):
        """get user by email or phone_number. disable case sensitive

        Args:
            field_name (string): field name is attribute from class User. eg: email, phone_number
            value (string): Value want to find. eg: "johndoe@example.com"

        Returns:
            queryset: User instance or None
        """
        filter_args = {f"{field_name}__iexact": value, "is_active": True}
        return get_user_model().objects.filter(**filter_args).last()

    def _validate_user_is_active(self, user):
        if not user.is_active:
            raise exceptions.AuthenticationFailed("User inactive or deleted")

    def _phone_number_format_is_valid(self, phone_number):
        # check with country_code
        try:
            phone_number_parsed = phone_number_parse("+" + phone_number)
        except NumberParseException:
            return False

        is_possible = is_possible_number(phone_number_parsed)
        is_valid = is_valid_number(phone_number_parsed)

        return is_possible == is_valid

    def _password_format_is_valid(self, raw_password):
        try:
            password_validation.validate_password(raw_password)
        except Exception as error:
            return False, error
        return True, None

    def _check_otp_or_hash_is_valid(self, method, value):
        if method == "email":
            verify_instance = EmailVerification.objects.filter(
                Q(code_hash=value) | Q(code=value),
                is_verified=False,
            ).last()
        else:
            verify_instance = PhoneVerification.objects.filter(
                is_verified=False, code=value
            ).last()

        if not verify_instance:
            raise custom_exceptions.InvalidVerificationCode

        if USE_VERIFY_EXPIRED:
            utc_now = datetime.datetime.utcnow()
            expired = utc_now - EXPIRED_TOKEN_TIMEDELTA

            if not self._time_is_valid(
                verify_instance.created_at, operator.lt, expired
            ):
                raise custom_exceptions.ExpiredVerificationCode
        return verify_instance

    def generate_new_token(self, user):
        utc_now = datetime.datetime.utcnow()

        token = Token.objects.filter(user=user).last()
        if not token:
            token = Token.objects.create(user=user)
        created_at_token = token.created

        # renew token if token expired
        if USE_TOKEN_EXPIRED and created_at_token < (utc_now - EXPIRED_TOKEN_TIMEDELTA):
            token.key = token.generate_key()
            token.created_at = utc_now
            token.save()

        return token

    def oauth_login(self, view_request, access_token, oauth_backend):
        """auth using oauth vendor. google, facebook, linkedin, etc

        Args:
            view_request (django view request): got from django views. eg: def create(self, request): .... _get_user_from_oauth_login(request, .....)
            access_token (string): access token got from vendor API
            oauth_backend (string): oauth backend want to be use. eg: google-oauth2

        Returns:
            queryset: return user instance
        """
        redirect_uri = OAUTH_REDIRECT_URI

        view_request.social_strategy = load_strategy(view_request)

        if not hasattr(view_request, "strategy"):
            view_request.strategy = view_request.social_strategy

        view_request.backend = load_backend(
            view_request.social_strategy, oauth_backend, redirect_uri
        )
        user = view_request.backend.do_auth(access_token)

        return user

    def password_login(self, username_field, username, raw_password):
        user_with_username_exist = self._get_user(username_field, username)
        if not user_with_username_exist:
            exceptions.AuthenticationFailed("Username and password is missmatch")

        # authenticate with password
        auth_kwargs = {
            "phone_number": user_with_username_exist.phone_number,
            "password": raw_password,
        }
        user = authenticate(**auth_kwargs)

        return self.generate_new_token(user)

    def service_account_login(self, token):
        pass

    def check_token_is_valid(self, key):
        try:
            token = Token.objects.get(key=key)
        except Token.DoesNotExist:
            raise exceptions.AuthenticationFailed("Invalid token")

        # check if implement expired token
        utc_now = datetime.datetime.utcnow()
        created_at_token = token.created
        expired = utc_now - EXPIRED_TOKEN_TIMEDELTA
        if USE_TOKEN_EXPIRED and self._time_is_valid(
            created_at_token, operator.lt, expired
        ):
            raise exceptions.AuthenticationFailed("Token has expired")

        # user is_active
        user = token.user
        self._validate_user_is_active(user)

        return user

    def basic_register(self, email, phone_number, full_name, password):
        email_lower = email.lower()
        user = self._get_user("email", email_lower)

        # always attach country code w/o + (plus). eg: 628123456789
        if not self._phone_number_format_is_valid(phone_number):
            raise custom_exceptions.InvalidPhoneNumberFormat

        password_is_valid, error = self._password_format_is_valid(password)
        if not password_is_valid:
            raise exceptions.ValidationError(error)

        if not user:
            user = self._get_user("phone_number", phone_number)

        if user and user.phone_number == phone_number:
            raise custom_exceptions.PhoneNumberAlreadyExist(phone_number)
        elif user and user.email.lower() == email_lower:
            raise custom_exceptions.EmailAlreadyExist(email_lower)

        user = get_user_model().objects.create(
            full_name=full_name, email=email_lower, phone_number=phone_number
        )
        user.set_password(password)
        user.save()

    def send_email_verification(
        self, user, subject_template_name, html_email_template_name
    ):
        email_template_name = html_email_template_name
        code = generate_otp_code(6)
        code_hash = str(uuid.uuid4())

        base_url = getattr(settings, "BASE_URL")
        frontend_base_url = (
            getattr(settings, "FRONTEND_BASE_URL")
            if hasattr(settings, "FRONTEND_BASE_URL")
            else base_url
        )

        if not code:
            code = str(uuid)
        email_verif = EmailVerification.objects.create(
            code=code, code_hash=code_hash, user=user, is_verified=False
        )

        # sending email here
        email = email_verif.user.email
        context = {
            "code": code,
            "code_hash": code_hash,
            "name": user.full_name,
            "base_url": base_url,
            "frontend_base_url": frontend_base_url,
        }
        send_mail(
            subject_template_name,
            email_template_name,
            html_email_template_name,
            context,
            email,
            cc=getattr(settings, "MAIL_NOTIFICATION_CC", []),
        )

        return email_verif, {"code": code, "code_hash": code_hash}

    def send_phone_verification(self, user, code=None):
        otp_manager = OTPManager(
            phone_number=user.phone_number,
            brand=OTP_BRAND,
            otp_length=OTP_CODE_LENGTH,
            template=OTP_TEMPLATE,
        )
        session_id, error = otp_manager.request_otp()

        if error:
            raise custom_exceptions.ErrorSendingOTP(error)

        phone_verif = PhoneVerification.objects.create(
            code=session_id, user=user, phone_number=user.phone_number
        )

        return phone_verif, session_id

    def verify_user(self, method, value):
        verify_instance = self._check_otp_or_hash_is_valid(method, value)

        # activate user by VERIFY_USER_METHODS
        methods_verified = []
        user = None
        for method_ in VERIFY_USER_METHODS:
            if method_ == "email":
                verify_instance = EmailVerification.objects.filter(
                    user=verify_instance.user
                ).last()
            else:
                verify_instance = PhoneVerification.objects.filter(
                    user=verify_instance.user
                ).last()

            is_verified = verify_instance and verify_instance.is_verified

            if is_verified:
                user = verify_instance.user
                methods_verified.append(is_verified)

        # raise error if verification not found
        if not user:
            raise custom_exceptions.InvalidVerificationCode

        # activate user if all methods verified. (based on VERIFY_USER_METHODS)
        user_is_verified = True
        for mv in methods_verified:
            user_is_verified = user_is_verified == mv

        if user_is_verified:
            user.is_active = True
            user.save()

    def check_current_password(self, user, current_password):
        return user.check_password(current_password)

    def set_passoword(self, user, raw_password):
        password_is_valid, error = self._password_format_is_valid(raw_password)
        if not password_is_valid:
            raise exceptions.ValidationError(error)

        user.set_password(raw_password)
        user.save()
