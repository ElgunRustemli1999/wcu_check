from django.apps import AppConfig


class FaceConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "face"
    
    def ready(self):
        # Signals-i import edirik, beləliklə, worker modeli ilə əlaqəli üz tanıma siqnalları işləyəcək
        import face.signals