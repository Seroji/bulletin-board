from django import template

from ..models import PostUserFavourite


register = template.Library()


@register.filter
def total_followers(args):
    total = PostUserFavourite.objects.filter(post_id=args).count()
    return total
