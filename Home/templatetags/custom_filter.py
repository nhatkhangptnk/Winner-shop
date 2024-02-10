from Home.models import *
from django import template

register = template.Library()


@register.filter
def GetChild(parentId):
    return Category.objects.filter(cate_parent_id=parentId)


@register.filter
def HaveChild(parentId):
    child = Category.objects.filter(cate_parent_id=parentId)
    if child is not None:
        if len(child) > 0:
            return True
    else:
        return False
