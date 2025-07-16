from django.apps import AppConfig


class AiInsightsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ai_insights'
    verbose_name = 'AI Clinical Insights'
    
    def ready(self):
        # Import signals or other startup code here if needed
        pass
