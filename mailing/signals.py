from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from mailing.models import Mailing
from mailing.tasks import start_maillist


@receiver(post_save, mailing=Mailing)
def start_maillist_task(mailing, instance, **kwargs):
    now = timezone.now()
    start_at = instance.start_at
    finish_at = instance.finish_at

    if (start_at <= now) and (finish_at > now):
        start_maillist.delay(instance.id)
    else:
        start_maillist.delay(instance.id, eta=start_at)
    return True