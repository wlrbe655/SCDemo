from django.apps import AppConfig

class App01Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app01'

    def ready(self):
        import app01.signals  # 注册缓存清理信号