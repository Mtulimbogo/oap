from django import template
from django.contrib.auth.models import Group

register = template.Library()


@register.filter(name='has_group')
def has_group(user, group_name):
    """
    --> usage: 


    {% load group_tags %}
    ...
    ...
    {% if request.user|has_group:"yourgroupe" %}
    # part which will only accessible for users registered in `yourgroup` 
    {% endif %} 

    """
    group = Group.objects.filter(name=group_name)
    if group:
        group = group.first()
        return group in user.groups.all()
    else:
        return False
