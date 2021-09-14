from django import template
from notification.models import Notification
register = template.Library()

@register.filter
def notification_count(user):
    if user.is_authenticated:
        qs = Notification.objects.filter(user=user, is_seen=False).count()
        return qs