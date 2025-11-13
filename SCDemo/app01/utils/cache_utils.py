from django.core.cache import cache

CACHE_KEYS = {
    'goods': ['sc_list_all', 'xcc_list_*'],
    'stu':   ['user_list_all'],
    'admin': ['admin_list_all'],
    'job':   ['job_list_all'],
    'order': ['order_list_all', 'user_orders_*'],
}

def clear_cache_for_model(model_name: str):
    """
    根据模型名自动清理相关缓存
    支持通配符 * 模糊删除
    """
    patterns = CACHE_KEYS.get(model_name, [])
    for pattern in patterns:
        if '*' in pattern:
            keys = cache.keys(pattern) or []
            for k in keys:
                cache.delete(k)
        else:
            cache.delete(pattern)