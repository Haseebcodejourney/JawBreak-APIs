from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'insights', views.AIInsightViewSet, basename='ai_insight')

app_name = 'ai_insights'

urlpatterns = [
    # Core AI Insights Management
    path('', include(router.urls)),
    
    # AI Processing Endpoints
    path('generate/', views.GenerateInsightsView.as_view(), name='generate_insights'),
    path('dashboard/', views.AIInsightDashboardView.as_view(), name='insights_dashboard'),
    
    # Specialized Analysis Endpoints (to be implemented)
    # path('trends/analyze/', views.TrendAnalysisView.as_view(), name='analyze_trends'),
    # path('risks/assess/', views.RiskAssessmentView.as_view(), name='assess_risks'),
    # path('documents/analyze/', views.DocumentAnalysisView.as_view(), name='analyze_document'),
    # path('communication/generate/', views.ProviderCommunicationView.as_view(), name='generate_communication'),
]
