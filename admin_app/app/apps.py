from django.apps import AppConfig


class AdminServiceAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'admin_app.app'
    label = 'admin_app'
    verbose_name = 'Admin Service'