from rest_framework import serializers
from .models import (
    AIInsight, PatientTrend, RiskPrediction, 
    ClinicalDecisionSupport, AIProcessingLog,
    AIInsightType, RiskLevel
)


class AIInsightSerializer(serializers.ModelSerializer):
    # Use SerializerMethodField to avoid import issues
    patient_name = serializers.SerializerMethodField()
    created_by_name = serializers.SerializerMethodField()
    reviewed_by_name = serializers.SerializerMethodField()
    is_critical = serializers.ReadOnlyField()
    days_since_created = serializers.ReadOnlyField()
    
    class Meta:
        model = AIInsight
        fields = [
            'id', 'patient', 'patient_name', 'visit', 'created_by', 'created_by_name',
            'insight_type', 'title', 'description', 'risk_level', 'priority_score', 
            'confidence_score', 'model_used', 'model_version', 
            'data_sources', 'evidence', 'is_actionable', 
            'recommended_actions', 'urgency_level', 'status', 
            'reviewed_by', 'reviewed_by_name', 'reviewed_at', 'review_notes', 
            'created_at', 'updated_at', 'expires_at',
            'is_critical', 'days_since_created'
        ]
        read_only_fields = ['created_at', 'updated_at', 'is_critical', 'days_since_created']
    
    def get_patient_name(self, obj):
        if obj.patient:
            return f"{obj.patient.first_name} {obj.patient.last_name}"
        return None
    
    def get_created_by_name(self, obj):
        if obj.created_by:
            return f"{obj.created_by.first_name} {obj.created_by.last_name}"
        return None
    
    def get_reviewed_by_name(self, obj):
        if obj.reviewed_by:
            return f"{obj.reviewed_by.first_name} {obj.reviewed_by.last_name}"
        return None


class AIInsightCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIInsight
        fields = [
            'patient', 'visit', 'insight_type', 'title', 'description',
            'risk_level', 'priority_score', 'confidence_score',
            'model_used', 'model_version', 'data_sources', 'evidence',
            'is_actionable', 'recommended_actions', 'urgency_level',
            'expires_at'
        ]
    
    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class PatientTrendSerializer(serializers.ModelSerializer):
    patient_name = serializers.SerializerMethodField()
    
    class Meta:
        model = PatientTrend
        fields = [
            'id', 'patient', 'patient_name', 'metric_name', 'metric_category',
            'trend_direction', 'trend_strength', 'statistical_significance',
            'data_points', 'analysis_period_days', 'ai_interpretation',
            'clinical_significance', 'created_at', 'updated_at', 'last_analyzed'
        ]
        read_only_fields = ['created_at', 'updated_at', 'last_analyzed']
    
    def get_patient_name(self, obj):
        if obj.patient:
            return f"{obj.patient.first_name} {obj.patient.last_name}"
        return None


class RiskPredictionSerializer(serializers.ModelSerializer):
    patient_name = serializers.SerializerMethodField()
    validated_by_name = serializers.SerializerMethodField()
    is_high_risk = serializers.ReadOnlyField()
    
    class Meta:
        model = RiskPrediction
        fields = [
            'id', 'patient', 'patient_name', 'risk_type', 'risk_score', 'risk_category',
            'confidence_interval', 'model_name', 'model_accuracy',
            'feature_importance', 'risk_factors', 'protective_factors',
            'prevention_strategies', 'monitoring_recommendations',
            'is_validated', 'validated_by', 'validated_by_name', 'validation_notes',
            'created_at', 'expires_at', 'is_high_risk'
        ]
        read_only_fields = ['created_at', 'is_high_risk']
    
    def get_patient_name(self, obj):
        if obj.patient:
            return f"{obj.patient.first_name} {obj.patient.last_name}"
        return None
    
    def get_validated_by_name(self, obj):
        if obj.validated_by:
            return f"{obj.validated_by.first_name} {obj.validated_by.last_name}"
        return None


class ClinicalDecisionSupportSerializer(serializers.ModelSerializer):
    patient_name = serializers.SerializerMethodField()
    reviewed_by_name = serializers.SerializerMethodField()
    
    class Meta:
        model = ClinicalDecisionSupport
        fields = [
            'id', 'patient', 'patient_name', 'visit', 'support_type', 'title',
            'recommendation', 'rationale', 'evidence_level',
            'current_status', 'proposed_changes', 'expected_outcomes',
            'potential_risks', 'urgency', 'requires_md_approval',
            'implementation_notes', 'status', 'reviewed_by', 'reviewed_by_name',
            'reviewed_at', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def get_patient_name(self, obj):
        if obj.patient:
            return f"{obj.patient.first_name} {obj.patient.last_name}"
        return None
    
    def get_reviewed_by_name(self, obj):
        if obj.reviewed_by:
            return f"{obj.reviewed_by.first_name} {obj.reviewed_by.last_name}"
        return None


class AIProcessingLogSerializer(serializers.ModelSerializer):
    patient_name = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()
    
    class Meta:
        model = AIProcessingLog
        fields = [
            'id', 'patient', 'patient_name', 'user', 'user_name', 'process_type', 'model_used',
            'input_data_size', 'processing_time_seconds', 'success',
            'error_message', 'output_summary', 'tokens_used',
            'cost_estimate', 'started_at', 'completed_at'
        ]
    
    def get_patient_name(self, obj):
        if obj.patient:
            return f"{obj.patient.first_name} {obj.patient.last_name}"
        return None
    
    def get_user_name(self, obj):
        if obj.user:
            return f"{obj.user.first_name} {obj.user.last_name}"
        return None


# Specialized serializers for API requests
class GenerateInsightRequestSerializer(serializers.Serializer):
    patient_id = serializers.IntegerField()
    insight_types = serializers.ListField(
        child=serializers.ChoiceField(choices=AIInsightType.choices),
        required=False,
        help_text="Types of insights to generate. If not provided, all types will be considered."
    )
    include_historical_data = serializers.BooleanField(default=True)
    analysis_period_days = serializers.IntegerField(default=30, min_value=1, max_value=365)


class TrendAnalysisRequestSerializer(serializers.Serializer):
    patient_id = serializers.IntegerField()
    metrics = serializers.ListField(
        child=serializers.CharField(max_length=100),
        help_text="List of metrics to analyze (e.g., 'blood_pressure', 'weight', 'pain_level')"
    )
    analysis_period_days = serializers.IntegerField(default=30, min_value=7, max_value=365)
    include_predictions = serializers.BooleanField(default=False)


class RiskAssessmentRequestSerializer(serializers.Serializer):
    patient_id = serializers.IntegerField()
    risk_types = serializers.ListField(
        child=serializers.ChoiceField(choices=[
            ('fall_risk', 'Fall Risk'),
            ('readmission_risk', 'Readmission Risk'),
            ('deterioration_risk', 'Deterioration Risk'),
            ('medication_adverse_event', 'Medication Adverse Event'),
            ('infection_risk', 'Infection Risk'),
            ('mortality_risk', 'Mortality Risk'),
            ('non_adherence_risk', 'Non-adherence Risk')
        ]),
        required=False,
        help_text="Types of risks to assess. If not provided, all applicable risks will be assessed."
    )
    include_recommendations = serializers.BooleanField(default=True)
    prediction_horizon_days = serializers.IntegerField(default=30, min_value=1, max_value=365)


class DocumentAnalysisRequestSerializer(serializers.Serializer):
    document_text = serializers.CharField()
    document_type = serializers.ChoiceField(choices=[
        ('visit_note', 'Visit Note'),
        ('discharge_summary', 'Discharge Summary'),
        ('lab_report', 'Lab Report'),
        ('imaging_report', 'Imaging Report'),
        ('consultation_note', 'Consultation Note'),
        ('assessment_form', 'Assessment Form'),
        ('other', 'Other')
    ])
    patient_id = serializers.IntegerField(required=False)
    extract_structured_data = serializers.BooleanField(default=True)
    generate_insights = serializers.BooleanField(default=False)


class ProviderCommunicationRequestSerializer(serializers.Serializer):
    patient_id = serializers.IntegerField()
    communication_type = serializers.ChoiceField(choices=[
        ('urgent_concern', 'Urgent Concern'),
        ('status_update', 'Status Update'),
        ('medication_question', 'Medication Question'),
        ('care_plan_update', 'Care Plan Update'),
        ('referral_request', 'Referral Request')
    ])
    specific_concerns = serializers.ListField(
        child=serializers.CharField(max_length=500),
        help_text="Specific concerns or questions to address"
    )
    urgency_level = serializers.ChoiceField(choices=[
        ('immediate', 'Immediate'),
        ('within_24h', 'Within 24 Hours'),
        ('within_week', 'Within Week'),
        ('routine', 'Routine')
    ], default='routine')
    include_recent_data = serializers.BooleanField(default=True)


# Response serializers
class AIInsightSummarySerializer(serializers.Serializer):
    """Summary of AI insights for dashboard view"""
    total_insights = serializers.IntegerField()
    critical_insights = serializers.IntegerField()
    new_insights = serializers.IntegerField()
    insights_by_type = serializers.DictField()
    insights_by_risk_level = serializers.DictField()
    recent_insights = AIInsightSerializer(many=True)


class TrendAnalysisResponseSerializer(serializers.Serializer):
    """Response format for trend analysis"""
    patient_id = serializers.IntegerField()
    analysis_period = serializers.CharField()
    trends_analyzed = serializers.IntegerField()
    significant_trends = serializers.ListField()
    ai_summary = serializers.CharField()
    recommendations = serializers.ListField()
    trends = PatientTrendSerializer(many=True)


class RiskAssessmentResponseSerializer(serializers.Serializer):
    """Response format for risk assessment"""
    patient_id = serializers.IntegerField()
    overall_risk_score = serializers.FloatField()
    highest_risk_category = serializers.CharField()
    critical_risks = serializers.ListField()
    recommended_interventions = serializers.ListField()
    risk_predictions = RiskPredictionSerializer(many=True)
