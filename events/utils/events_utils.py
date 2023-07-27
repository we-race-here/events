from django.conf import settings
from django.core.mail import send_mail


def sys_send_mail(
    subject, message, from_email=None, recipient_list=[], recipient_system=[], fail_silently=False, html_message=None
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
        recipient_list=recipient_system + settings.NOISY_EMAILS,
        html_message=html_message,
        fail_silently=fail_silently,
    )
