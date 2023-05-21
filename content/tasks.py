from celery import shared_task
from .mail import reply_user_inform, reply_apply_inform


@shared_task
def reply_info(post_id):
    reply_user_inform(post_id)

@shared_task
def apply_info(reply_id):
    reply_apply_inform(reply_id)
