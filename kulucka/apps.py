from django.apps import AppConfig

class KuluckaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'kulucka'
    # 📌 Admin panelindeki büyük mavi başlığı tamamen değiştirir:
    verbose_name = 'Zanaat-AI Hub Yönetimi'
