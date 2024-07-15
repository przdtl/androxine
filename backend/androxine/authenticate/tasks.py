import uuid

from django.conf import settings
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from celery import shared_task

from authenticate.services import EmailVerificationTokenGenerator

UserModel = get_user_model()


@shared_task()
def send_user_verifications_email(user_id: uuid.UUID, domain: str) -> None:
    '''
    Task for sending user verification email
    '''

    try:
        user = UserModel.objects.get(pk=user_id)
    except UserModel.DoesNotExist:
        return

    email = user.email
    username = user.username
    verification_token = EmailVerificationTokenGenerator().make_token(user)

    body_template_path = 'authenticate/user_verifications_email_body.html'
    body_template_context = {
        'uid': user_id,
        'username': username,
        'token': verification_token,
        'domain': domain,
    }

    body_template_string = render_to_string(
        template_name=body_template_path,
        context=body_template_context,
    )

    body_template_plain_message = strip_tags(body_template_string)

    send_mail(
        subject='',
        message=body_template_plain_message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email,],
        fail_silently=True,
    )
