from django import template

from ..models import PostUserFavourite, PostUserLike


register = template.Library()


@register.filter
def total_followers(args):
    total = PostUserFavourite.objects.filter(post_id=args).count()
    return total


@register.filter
def total_likes(args):
    total = PostUserLike.objects.filter(post_id=args).count()
    return total