from django.conf import settings
from django.core.mail import send_mail


def sys_send_mail(
    subject: str,
    message: str,
    from_email: str = None,
    recipient_list: list = [],
    recipient_system: list = [],
    fail_silently: bool = False,
    html_message: str = None,
):
    # send to user
    send_mail(
        subject=subject,
        message=message,
        from_email=from_email or settings.DJANGO_DEFAULT_FROM_EMAIL,
        recipient_list=recipient_list,
        html_message=html_message,
        fail_silently=fail_silently,
    )
    # send to admins
    send_mail(
        subject=subject,
        message=message,
        from_email=from_email or settings.DJANGO_DEFAULT_FROM_EMAIL,
        recipient_list=set(recipient_system + settings.NOISY_EMAILS),
        html_message=html_message,
        fail_silently=fail_silently,
    )
