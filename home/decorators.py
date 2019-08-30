from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import REDIRECT_FIELD_NAME

def employee_required(function=None,redirect_field_name=REDIRECT_FIELD_NAME, login_url='/'):

    actual_decorator = user_passes_test(lambda u: u.is_active and u.is_employee,
                                        login_url=login_url,
                                        redirect_field_name=redirect_field_name
                                        )
    if function:
        return actual_decorator(function)
    return actual_decorator

def HR_required(function=None,redirect_field_name=REDIRECT_FIELD_NAME, login_url='/'):

    actual_decorator = user_passes_test(lambda u: u.is_active and u.is_HR,
                                        login_url=login_url,
                                        redirect_field_name=redirect_field_name
                                        )
    if function:
        return actual_decorator(function)
    return actual_decorator