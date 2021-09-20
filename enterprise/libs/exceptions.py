from django.core.checks import messages
from django.utils.translation import gettext_lazy as _


class PhoneNumberAlreadyExist(Exception):
    message = _("Phone number already exists")

    def __init__(self, phone_number=None):
        if phone_number:
            self.message = _(f"{phone_number} already exists")
        super().__init__(self.message)


class EmailAlreadyExist(Exception):
    message = _("Email already exists")

    def __init__(self, email=None):
        if email:
            self.message = _(f"{email} already exists")
        super().__init__(self.message)


class InvalidVerificationCode(Exception):
    message = _("Verification code invalid")


class ExpiredVerificationCode(Exception):
    message = _("Verification code is expired")


class ErrorSendingOTP(Exception):
    message = _("Failed to send OTP")

    def __init__(self, message=None):
        if message:
            self.message = message
        super().__init__(self.message)


class ErrorValidateOTP(Exception):
    message = _("Failed to validate OTP")

    def __init__(self, message=None):
        if message:
            self.message = message
        super().__init__(self.message)


class InvalidPhoneNumberFormat(Exception):
    message = _("Invalid phone number format")

    def __init__(self, message=None):
        if message:
            self.message = message
        super().__init__(self.message)


class UserDoesNotExists(Exception):
    messages = _("User does not exists")


class InvalidOAuthBackend(Exception):
    messages = _("Invalid oauth backend")


class InvalidCodeOrHashVerification(Exception):
    messages = _("Invalid Code or Hash Verification")
