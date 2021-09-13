import re

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _


class UppercaseValidator(object):
    def validate(self, password, user=None):
        if not re.findall("[A-Z]", password):
            raise ValidationError(
                _("The password must contain at least 1 uppercase letter, A-Z."),
                code="password_no_upper",
            )

    def get_help_text(self):
        return _("Your password must contain at least 1 uppercase letter, A-Z.")


class AlfaNumericValidator(object):
    def validate(self, password, user=None):
        if not re.findall("^[0-9a-zA-Z]*$", password):
            raise ValidationError(
                _("The password must be alfa numeric"),
                code="password_no_alfa_numeric",
            )

    def get_help_text(self):
        return _("Your password must be alfa numeric")


class ComplexPasswordValidator:
    """
    Validate whether the password contains minimum one uppercase, one digit and one symbol.
    """

    def validate(self, password, user=None):
        if (
            re.search("[A-Z][a-z]", password) == None
            and re.search("[0-9]", password) == None
        ):
            raise ValidationError(
                _("The password must be alfa numeric"),
                code="password_no_alfa_numeric",
            )

    def get_help_text(self):
        return _("The password must be alfa numeric")
