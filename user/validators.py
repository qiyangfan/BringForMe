from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _


class PasswordValidator(RegexValidator):
    regex = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!"#$%&\'()*+,\-./:;<=>?@[\\\]^_`{|}~])[A-Za-z\d!"#$%&\'()*+,\-./:;<=>?@[\\\]^_`{|}~]{8,20}$'
    message = _(
        'Your password must be 8 to 20 characters long and include at least one uppercase letter, one lowercase letter, one number, and one special character from the following set: !"#$%%&\'()*+,-./:;<=>?@[\]^_{|}~`.')


class CountryCodeValidator(RegexValidator):
    regex = r'^\+?\d{1,3}$'
    message = _('Invalid country code format. Please enter a valid country code (e.g., +1, +86).')


class PhoneValidator(RegexValidator):
    regex = r'^\d{1,15}$'
    message = _('Invalid phone number format. Please enter a valid phone number with digits only.')
