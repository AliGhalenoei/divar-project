from django.core.exceptions import ValidationError

def validate_phone(value):
    if not value.startswith('09'):
        raise ValidationError('شماره تلفن وارد شده معتبر نیست')
    elif len(value) != 11:
        raise ValidationError('شماره تلفن باید یازده رقم باشد')