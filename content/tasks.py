from celery import shared_task
from .mail import reply_user_inform, reply_apply_inform, verify_code, advertisment


@shared_task
def reply_info(post_id):
    reply_user_inform(post_id)

@shared_task
def apply_info(reply_id):
    reply_apply_inform(reply_id)

@shared_task
def verify_email(user_id):
    verify_code(user_id)

@shared_task
def advert(subject, text_content):
    advertisment(subject, text_content)