from django.template import Library
from microblog.models import *
from settings import *

register=Library()

def inrelation(val,relation):
    return val in relation

register.filter("inrelation",inrelation)