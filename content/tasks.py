from celery import shared_task
from .mail import reply_user_inform


@shared_task
def reply_info(post_id):
    reply_user_inform(post_id)
