from django import template

from ..models import PostUserFavourite, PostUserLike, PostCategory, Category


register = template.Library()


@register.filter
def total_followers(args):
    total = PostUserFavourite.objects.filter(post_id=args).count()
    return total


@register.filter
def total_likes(args):
    total = PostUserLike.objects.filter(post_id=args).count()
    if total:
        return total
    else:
        return 0
    

@register.filter
def define_category(args):
    category = PostCategory.objects.get(post_id=args)
    cat_id = category.category_id
    cat = Category.objects.get(pk=cat_id)
    return cat.category
