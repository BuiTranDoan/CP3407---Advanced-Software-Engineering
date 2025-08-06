from django.contrib.auth.decorators import user_passes_test

def admin_required(view_func):
    return user_passes_test(lambda u: u.is_authenticated and u.is_superuser)(view_func)

def counter_required(view_func):
    return user_passes_test(lambda u: u.is_authenticated and u.is_staff and not u.is_superuser)(view_func)
