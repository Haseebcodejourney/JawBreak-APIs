from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Q, Count
from datetime import timedelta
import logging

from .models import (
    AIInsight, PatientTrend, RiskPrediction, 
    ClinicalDecisionSupport, AIProcessingLog
)
from .serializers import (
    AIInsightSerializer, AIInsightCreateSerializer,
    PatientTrendSerializer, RiskPredictionSerializer,
    ClinicalDecisionSupportSerializer, AIProcessingLogSerializer,
    GenerateInsightRequestSerializer, TrendAnalysisRequestSerializer,
    RiskAssessmentRequestSerializer, DocumentAnalysisRequestSerializer,
    ProviderCommunicationRequestSerializer, AIInsightSummarySerializer,
    TrendAnalysisResponseSerializer, RiskAssessmentResponseSerializer
)
from .ai_services import (
    clinical_insight_generator, risk_assessment_engine,
    trend_analyzer, document_analyzer
)
from django.apps import apps

# Get models dynamically to avoid import issues
Patient = apps.get_model('patients', 'Patient')
Visit = apps.get_model('visits', 'Visit')

logger = logging.getLogger('ai_insights')


class AIInsightViewSet(viewsets.ModelViewSet):
    """ViewSet for managing AI insights"""
    queryset = AIInsight.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return AIInsightCreateSerializer
        return AIInsightSerializer
    
    def get_queryset(self):
        queryset = AIInsight.objects.all()
        
        # Filter by patient
        patient_id = self.request.query_params.get('patient_id', None)
        if patient_id:
            queryset = queryset.filter(patient_id=patient_id)
        
        # Filter by insight type
        insight_type = self.request.query_params.get('insight_type', None)
        if insight_type:
            queryset = queryset.filter(insight_type=insight_type)
        
        # Filter by risk level
        risk_level = self.request.query_params.get('risk_level', None)
        if risk_level:
            queryset = queryset.filter(risk_level=risk_level)
        
        # Filter by status
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Filter critical insights
        critical_only = self.request.query_params.get('critical_only', None)
        if critical_only and critical_only.lower() == 'true':
            queryset = queryset.filter(
                Q(risk_level='critical') | Q(urgency_level='immediate')
            )
        
        return queryset.order_by('-priority_score', '-created_at')
    
    @action(detail=True, methods=['post'])
    def mark_reviewed(self, request, pk=None):
        """Mark an insight as reviewed"""
        insight = self.get_object()
        insight.status = 'reviewed'
        insight.reviewed_by = request.user
        insight.reviewed_at = timezone.now()
        insight.review_notes = request.data.get('review_notes', '')
        insight.save()
        
        return Response({'status': 'Insight marked as reviewed'})
    
    @action(detail=True, methods=['post'])
    def dismiss(self, request, pk=None):
        """Dismiss an insight"""
        insight = self.get_object()
        insight.status = 'dismissed'
        insight.reviewed_by = request.user
        insight.reviewed_at = timezone.now()
        insight.review_notes = request.data.get('reason', '')
        insight.save()
        
        return Response({'status': 'Insight dismissed'})


class GenerateInsightsView(APIView):
    """Generate AI insights for a patient"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = GenerateInsightRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        data = serializer.validated_data
        patient = get_object_or_404(Patient, id=data['patient_id'])
        
        try:
            # Collect patient data
            patient_data = self._collect_patient_data(
                patient, 
                data.get('include_historical_data', True),
                data.get('analysis_period_days', 30)
            )
            
            # Generate insights using AI
            ai_response = clinical_insight_generator.generate_patient_summary(patient_data)
            
            if ai_response.success:
                # Process and save insights
                insights = self._process_ai_insights(
                    patient, ai_response, request.user, data.get('insight_types', [])
                )
                
                return Response({
                    'success': True,
                    'insights_generated': len(insights),
                    'insights': AIInsightSerializer(insights, many=True).data
                })
            else:
                return Response({
                    'error': 'Failed to generate insights',
                    'details': ai_response.error_message
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
        except Exception as e:
            logger.error(f"Error generating insights: {str(e)}")
            return Response({
                'error': 'Internal server error'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def _collect_patient_data(self, patient, include_historical, days):
        """Collect comprehensive patient data for analysis"""
        data = {
            'patient_id': patient.id,
            'demographics': {
                'age': patient.age if hasattr(patient, 'age') else None,
                'gender': patient.gender if hasattr(patient, 'gender') else None,
            },
            'conditions': [],
            'medications': [],
            'recent_visits': [],
            'vital_signs': [],
            'assessments': []
        }
        
        if include_historical:
            # Get recent visits
            recent_visits = patient.visits.filter(
                visit_date__gte=timezone.now() - timedelta(days=days)
            ).order_by('-visit_date')[:10]
            
            for visit in recent_visits:
                visit_data = {
                    'date': visit.visit_date.isoformat(),
                    'type': visit.visit_type if hasattr(visit, 'visit_type') else 'unknown',
                    'notes': visit.notes if hasattr(visit, 'notes') else '',
                }
                data['recent_visits'].append(visit_data)
        
        return data
    
    def _process_ai_insights(self, patient, ai_response, user, insight_types):
        """Process AI response and create insight objects"""
        insights = []
        
        try:
            # Parse AI response - assuming it returns structured insights
            ai_content = ai_response.content
            
            # Create a general insight from the AI response
            insight = AIInsight.objects.create(
                patient=patient,
                created_by=user,
                insight_type='risk_assessment',  # Default type
                title='AI-Generated Patient Analysis',
                description=ai_content,
                risk_level='low',  # Default, should be determined by AI
                priority_score=0.5,  # Default
                confidence_score=ai_response.confidence,
                model_used=ai_response.model_used,
                data_sources=['patient_data', 'visit_history'],
                evidence={'ai_analysis': ai_content},
                is_actionable=True,
                recommended_actions=['Review AI analysis', 'Consider clinical correlation'],
                urgency_level='routine'
            )
            insights.append(insight)
            
        except Exception as e:
            logger.error(f"Error processing AI insights: {str(e)}")
        
        return insights


class AIInsightDashboardView(APIView):
    """Dashboard view for AI insights summary"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        patient_id = request.query_params.get('patient_id')
        
        # Base queryset
        insights_qs = AIInsight.objects.all()
        if patient_id:
            insights_qs = insights_qs.filter(patient_id=patient_id)
        
        # Calculate summary statistics
        total_insights = insights_qs.count()
        critical_insights = insights_qs.filter(
            Q(risk_level='critical') | Q(urgency_level='immediate')
        ).count()
        new_insights = insights_qs.filter(status='new').count()
        
        # Insights by type
        insights_by_type = dict(
            insights_qs.values_list('insight_type').annotate(count=Count('id'))
        )
        
        # Insights by risk level
        insights_by_risk_level = dict(
            insights_qs.values_list('risk_level').annotate(count=Count('id'))
        )
        
        # Recent insights
        recent_insights = insights_qs.order_by('-created_at')[:10]
        
        summary_data = {
            'total_insights': total_insights,
            'critical_insights': critical_insights,
            'new_insights': new_insights,
            'insights_by_type': insights_by_type,
            'insights_by_risk_level': insights_by_risk_level,
            'recent_insights': AIInsightSerializer(recent_insights, many=True).data
        }
        
        return Response(summary_data)
