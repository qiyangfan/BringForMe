from django.core.validators import RegexValidator


class PasswordValidator(RegexValidator):
    regex = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,20}$'
    message = 'Your password must be 8-20 characters long and include at least one uppercase letter, one lowercase letter, one number, and one special character (!@#$%%^&*).'
