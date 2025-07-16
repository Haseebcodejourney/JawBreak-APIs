from django.contrib import admin
from .models import (
    AIInsight, PatientTrend, RiskPrediction, 
    ClinicalDecisionSupport, AIProcessingLog
)


@admin.register(AIInsight)
class AIInsightAdmin(admin.ModelAdmin):
    list_display = ['patient', 'title', 'insight_type', 'risk_level', 'priority_score', 'status', 'created_at']
    list_filter = ['insight_type', 'risk_level', 'status', 'urgency_level', 'created_at']
    search_fields = ['patient__first_name', 'patient__last_name', 'title', 'description']
    readonly_fields = ['created_at', 'updated_at', 'is_critical', 'days_since_created']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('patient', 'visit', 'created_by', 'insight_type', 'title', 'description')
        }),
        ('Risk Assessment', {
            'fields': ('risk_level', 'priority_score', 'confidence_score', 'urgency_level')
        }),
        ('AI Model Information', {
            'fields': ('model_used', 'model_version', 'data_sources', 'evidence')
        }),
        ('Actionability', {
            'fields': ('is_actionable', 'recommended_actions')
        }),
        ('Review Status', {
            'fields': ('status', 'reviewed_by', 'reviewed_at', 'review_notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'expires_at', 'is_critical', 'days_since_created'),
            'classes': ('collapse',)
        })
    )


@admin.register(PatientTrend)
class PatientTrendAdmin(admin.ModelAdmin):
    list_display = ['patient', 'metric_name', 'metric_category', 'trend_direction', 'trend_strength', 'last_analyzed']
    list_filter = ['metric_category', 'trend_direction', 'last_analyzed']
    search_fields = ['patient__first_name', 'patient__last_name', 'metric_name']
    readonly_fields = ['created_at', 'updated_at', 'last_analyzed']


@admin.register(RiskPrediction)
class RiskPredictionAdmin(admin.ModelAdmin):
    list_display = ['patient', 'risk_type', 'risk_score', 'risk_category', 'is_validated', 'created_at']
    list_filter = ['risk_type', 'risk_category', 'is_validated', 'created_at']
    search_fields = ['patient__first_name', 'patient__last_name']
    readonly_fields = ['created_at', 'is_high_risk']


@admin.register(ClinicalDecisionSupport)
class ClinicalDecisionSupportAdmin(admin.ModelAdmin):
    list_display = ['patient', 'title', 'support_type', 'urgency', 'status', 'requires_md_approval', 'created_at']
    list_filter = ['support_type', 'urgency', 'status', 'requires_md_approval', 'created_at']
    search_fields = ['patient__first_name', 'patient__last_name', 'title', 'recommendation']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(AIProcessingLog)
class AIProcessingLogAdmin(admin.ModelAdmin):
    list_display = ['process_type', 'model_used', 'success', 'processing_time_seconds', 'tokens_used', 'completed_at']
    list_filter = ['process_type', 'success', 'completed_at']
    search_fields = ['patient__first_name', 'patient__last_name', 'model_used']
    readonly_fields = ['started_at', 'completed_at']
