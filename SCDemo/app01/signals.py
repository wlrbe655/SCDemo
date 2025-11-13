from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import goods, Stu, admin, job, order
from .utils.cache_utils import clear_cache_for_model

MODEL_MAP = {
    goods: 'goods',
    Stu:   'stu',
    admin: 'admin',
    job:   'job',
    order: 'order',
}

@receiver([post_save, post_delete])
def auto_clear_cache(sender, **kwargs):
    model_name = MODEL_MAP.get(sender)
    if model_name:
        clear_cache_for_model(model_name)