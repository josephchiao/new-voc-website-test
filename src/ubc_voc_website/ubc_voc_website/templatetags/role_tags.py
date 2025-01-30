from django import template
from utils import *

register = template.Library()

@register.filter(name='is_member')
def is_member(user):
    return user.is_authenticated and is_member(user)

@register.filter(name='is_exec')
def is_exec(user):
    return user.is_authenticated and is_exec(user)

@register.filter(name='is_psg')
def is_psg(user):
    return user.is_authenticated and is_PSG(user)
