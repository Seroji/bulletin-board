from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth.models import User

from .models import Post, Reply, EmailAddresses


def reply_user_inform(post_id):
    post = Post.objects.get(id=post_id)
    to_email = post.author.email
    subject, from_email, to = 'Поступил отклик!', 'gamexr6@mail.ru', f'{to_email}'
    html_content = render_to_string('mail/reply_user_inform.html', {'post': post})
    text_content = strip_tags(html_content)

    msg = EmailMultiAlternatives(
        subject,
        text_content,
        from_email,
        [to_email]
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()

def reply_apply_inform(reply_id):
    reply = Reply.objects.get(id=reply_id)
    to_email = reply.author.email
    subject, from_email, to = 'Ваш отклик приняли!', 'gamexr6@mail.ru', f'{to_email}'
    html_content = render_to_string('mail/reply_apply_inform.html', {'reply': reply})
    text_content = strip_tags(html_content)

    msg = EmailMultiAlternatives(
        subject,
        text_content,
        from_email,
        [to_email]
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


def verify_code(user_id):
    instance = EmailAddresses.objects.get(user_id=user_id)
    otp = instance.otp
    user = User.objects.get(id=user_id)
    to_email = user.email
    subject, from_email, to = 'Проверочный код', 'gamexr6@mail.ru', to_email
    html_content = render_to_string('mail/verify_code.html', {'otp': otp})
    text_content = strip_tags(html_content)

    msg = EmailMultiAlternatives(
        subject,
        text_content,
        from_email,
        [to_email]
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()
