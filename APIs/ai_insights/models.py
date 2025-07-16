from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
import json

User = get_user_model()


class AIInsightType(models.TextChoices):
    RISK_ASSESSMENT = 'risk_assessment', 'Risk Assessment'
    TREND_ANALYSIS = 'trend_analysis', 'Trend Analysis'
    ANOMALY_DETECTION = 'anomaly_detection', 'Anomaly Detection'
    MEDICATION_INTERACTION = 'medication_interaction', 'Medication Interaction'
    CARE_GAP = 'care_gap', 'Care Gap'
    DOCUMENTATION_SUGGESTION = 'documentation_suggestion', 'Documentation Suggestion'
    PROVIDER_COMMUNICATION = 'provider_communication', 'Provider Communication'
    QUALITY_INDICATOR = 'quality_indicator', 'Quality Indicator'


class RiskLevel(models.TextChoices):
    LOW = 'low', 'Low'
    MODERATE = 'moderate', 'Moderate'
    HIGH = 'high', 'High'
    CRITICAL = 'critical', 'Critical'


class AIInsight(models.Model):
    """Core model for storing AI-generated insights"""
    # Use string references to avoid circular imports
    patient = models.ForeignKey('patients.Patient', on_delete=models.CASCADE, related_name='ai_insights')
    visit = models.ForeignKey('visits.Visit', on_delete=models.CASCADE, null=True, blank=True, related_name='ai_insights')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Insight Classification
    insight_type = models.CharField(max_length=50, choices=AIInsightType.choices)
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    # Risk and Priority
    risk_level = models.CharField(max_length=20, choices=RiskLevel.choices, default=RiskLevel.LOW)
    priority_score = models.FloatField(default=0.0, help_text="0-1 scale, 1 being highest priority")
    confidence_score = models.FloatField(default=0.0, help_text="0-1 scale, 1 being highest confidence")
    
    # AI Model Information
    model_used = models.CharField(max_length=100, help_text="AI model that generated this insight")
    model_version = models.CharField(max_length=50, blank=True)
    
    # Data Sources
    data_sources = models.JSONField(default=list, help_text="List of data sources used for this insight")
    evidence = models.JSONField(default=dict, help_text="Supporting evidence and data points")
    
    # Actionability
    is_actionable = models.BooleanField(default=True)
    recommended_actions = models.JSONField(default=list, help_text="List of recommended actions")
    urgency_level = models.CharField(max_length=20, choices=[
        ('immediate', 'Immediate'),
        ('within_24h', 'Within 24 Hours'),
        ('within_week', 'Within Week'),
        ('routine', 'Routine')
    ], default='routine')
    
    # Status and Follow-up
    status = models.CharField(max_length=20, choices=[
        ('new', 'New'),
        ('reviewed', 'Reviewed'),
        ('acted_upon', 'Acted Upon'),
        ('dismissed', 'Dismissed'),
        ('resolved', 'Resolved')
    ], default='new')
    
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_insights')
    reviewed_at = models.DateTimeField(null=True, blank=True)
    review_notes = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField(null=True, blank=True, help_text="When this insight becomes outdated")
    
    class Meta:
        ordering = ['-priority_score', '-created_at']
        indexes = [
            models.Index(fields=['patient', 'insight_type']),
            models.Index(fields=['risk_level', 'status']),
            models.Index(fields=['created_at', 'priority_score']),
        ]
    
    def __str__(self):
        return f"Patient #{self.patient_id} - {self.title} ({self.get_risk_level_display()})"
    
    @property
    def is_critical(self):
        return self.risk_level == RiskLevel.CRITICAL or self.urgency_level == 'immediate'
    
    @property
    def days_since_created(self):
        from django.utils import timezone
        return (timezone.now() - self.created_at).days


class PatientTrend(models.Model):
    """Track trends in patient data over time"""
    patient = models.ForeignKey('patients.Patient', on_delete=models.CASCADE, related_name='trends')
    
    # Trend Information
    metric_name = models.CharField(max_length=100, help_text="Name of the metric being tracked")
    metric_category = models.CharField(max_length=50, choices=[
        ('vital_signs', 'Vital Signs'),
        ('functional_status', 'Functional Status'),
        ('pain_levels', 'Pain Levels'),
        ('medication_adherence', 'Medication Adherence'),
        ('mobility', 'Mobility'),
        ('cognitive_status', 'Cognitive Status'),
        ('wound_healing', 'Wound Healing'),
        ('lab_values', 'Lab Values')
    ])
    
    # Trend Analysis
    trend_direction = models.CharField(max_length=20, choices=[
        ('improving', 'Improving'),
        ('stable', 'Stable'),
        ('declining', 'Declining'),
        ('fluctuating', 'Fluctuating')
    ])
    
    trend_strength = models.FloatField(help_text="Strength of trend, 0-1 scale")
    statistical_significance = models.FloatField(null=True, blank=True, help_text="P-value if applicable")
    
    # Data Points
    data_points = models.JSONField(default=list, help_text="Time series data points")
    analysis_period_days = models.IntegerField(default=30)
    
    # AI Analysis
    ai_interpretation = models.TextField(help_text="AI-generated interpretation of the trend")
    clinical_significance = models.TextField(help_text="Clinical significance of this trend")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_analyzed = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['patient', 'metric_name', 'metric_category']
        ordering = ['-trend_strength', '-updated_at']
    
    def __str__(self):
        return f"Patient #{self.patient_id} - {self.metric_name} ({self.trend_direction})"


class RiskPrediction(models.Model):
    """Store AI-generated risk predictions for patients"""
    patient = models.ForeignKey('patients.Patient', on_delete=models.CASCADE, related_name='risk_predictions')
    
    # Risk Type
    risk_type = models.CharField(max_length=50, choices=[
        ('fall_risk', 'Fall Risk'),
        ('readmission_risk', 'Readmission Risk'),
        ('deterioration_risk', 'Deterioration Risk'),
        ('medication_adverse_event', 'Medication Adverse Event'),
        ('infection_risk', 'Infection Risk'),
        ('mortality_risk', 'Mortality Risk'),
        ('non_adherence_risk', 'Non-adherence Risk')
    ])
    
    # Prediction Details
    risk_score = models.FloatField(help_text="Risk score 0-1, 1 being highest risk")
    risk_category = models.CharField(max_length=20, choices=RiskLevel.choices)
    confidence_interval = models.JSONField(default=dict, help_text="Confidence intervals for the prediction")
    
    # Model Information
    model_name = models.CharField(max_length=100)
    model_accuracy = models.FloatField(null=True, blank=True, help_text="Model accuracy on validation set")
    feature_importance = models.JSONField(default=dict, help_text="Most important features for this prediction")
    
    # Contributing Factors
    risk_factors = models.JSONField(default=list, help_text="List of risk factors identified")
    protective_factors = models.JSONField(default=list, help_text="List of protective factors identified")
    
    # Recommendations
    prevention_strategies = models.JSONField(default=list, help_text="AI-recommended prevention strategies")
    monitoring_recommendations = models.JSONField(default=list, help_text="What to monitor closely")
    
    # Validation
    is_validated = models.BooleanField(default=False)
    validated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    validation_notes = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(help_text="When this prediction expires")
    
    class Meta:
        ordering = ['-risk_score', '-created_at']
        indexes = [
            models.Index(fields=['patient', 'risk_type']),
            models.Index(fields=['risk_category', 'created_at']),
        ]
    
    def __str__(self):
        return f"Patient #{self.patient_id} - {self.get_risk_type_display()} ({self.risk_score:.2f})"
    
    @property
    def is_high_risk(self):
        return self.risk_score >= 0.7 or self.risk_category in ['high', 'critical']


class ClinicalDecisionSupport(models.Model):
    """AI-generated clinical decision support recommendations"""
    patient = models.ForeignKey('patients.Patient', on_delete=models.CASCADE, related_name='decision_support')
    visit = models.ForeignKey('visits.Visit', on_delete=models.CASCADE, null=True, blank=True)
    
    # Decision Support Type
    support_type = models.CharField(max_length=50, choices=[
        ('medication_adjustment', 'Medication Adjustment'),
        ('care_plan_modification', 'Care Plan Modification'),
        ('referral_recommendation', 'Referral Recommendation'),
        ('diagnostic_suggestion', 'Diagnostic Suggestion'),
        ('intervention_recommendation', 'Intervention Recommendation'),
        ('monitoring_frequency', 'Monitoring Frequency')
    ])
    
    # Content
    title = models.CharField(max_length=200)
    recommendation = models.TextField()
    rationale = models.TextField()
    evidence_level = models.CharField(max_length=20, choices=[
        ('high', 'High Quality Evidence'),
        ('moderate', 'Moderate Quality Evidence'),
        ('low', 'Low Quality Evidence'),
        ('expert_opinion', 'Expert Opinion/AI Analysis')
    ])
    
    # Clinical Information
    current_status = models.TextField()
    proposed_changes = models.JSONField(default=list)
    expected_outcomes = models.JSONField(default=list)
    potential_risks = models.JSONField(default=list)
    
    # Implementation
    urgency = models.CharField(max_length=20, choices=[
        ('immediate', 'Immediate'),
        ('within_24h', 'Within 24 Hours'),
        ('within_week', 'Within Week'),
        ('next_visit', 'Next Visit'),
        ('routine', 'Routine')
    ])
    
    requires_md_approval = models.BooleanField(default=True)
    implementation_notes = models.TextField(blank=True)
    
    # Status
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('implemented', 'Implemented'),
        ('declined', 'Declined'),
        ('modified', 'Modified')
    ], default='pending')
    
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Patient #{self.patient_id} - {self.title}"


class AIProcessingLog(models.Model):
    """Log AI processing activities for audit and debugging"""
    patient = models.ForeignKey('patients.Patient', on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Processing Information
    process_type = models.CharField(max_length=50, choices=[
        ('insight_generation', 'Insight Generation'),
        ('risk_assessment', 'Risk Assessment'),
        ('trend_analysis', 'Trend Analysis'),
        ('decision_support', 'Decision Support'),
        ('document_analysis', 'Document Analysis'),
        ('data_extraction', 'Data Extraction')
    ])
    
    model_used = models.CharField(max_length=100)
    input_data_size = models.IntegerField(help_text="Size of input data in bytes")
    processing_time_seconds = models.FloatField()
    
    # Results
    success = models.BooleanField(default=True)
    error_message = models.TextField(blank=True)
    output_summary = models.JSONField(default=dict)
    
    # Resource Usage
    tokens_used = models.IntegerField(null=True, blank=True)
    cost_estimate = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    
    # Timestamps
    started_at = models.DateTimeField()
    completed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-completed_at']
    
    def __str__(self):
        status = "Success" if self.success else "Failed"
        return f"{self.process_type} - {status} ({self.processing_time_seconds:.2f}s)"
