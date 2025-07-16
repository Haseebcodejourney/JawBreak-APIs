"""
AI Services for Clinical Insight Platform
Provides core AI functionality including:
- OpenAI/GPT integration
- Medical NLP processing
- Risk assessment algorithms
- Trend analysis
- Clinical decision support
"""

import openai
import logging
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from django.conf import settings
from django.utils import timezone
from .models import AIInsight, PatientTrend, RiskPrediction, ClinicalDecisionSupport, AIProcessingLog
import json
import re
from dataclasses import dataclass

logger = logging.getLogger('ai_insights')


@dataclass
class AIResponse:
    """Structured response from AI processing"""
    success: bool
    content: str
    confidence: float
    model_used: str
    tokens_used: int = 0
    processing_time: float = 0.0
    error_message: str = ""


class AIServiceManager:
    """Main AI service manager for healthcare insights"""
    
    def __init__(self):
        self._openai_client = None
        self.default_model = getattr(settings, 'AI_CONFIG', {}).get('DEFAULT_MODEL', 'gpt-4o-mini')
        self.max_tokens = getattr(settings, 'AI_CONFIG', {}).get('MAX_TOKENS', 4000)
        self.temperature = getattr(settings, 'AI_CONFIG', {}).get('TEMPERATURE', 0.3)
    
    @property
    def openai_client(self):
        """Lazy initialization of OpenAI client"""
        if self._openai_client is None:
            api_key = getattr(settings, 'OPENAI_API_KEY', None)
            if api_key and api_key != 'your-openai-api-key-here':
                try:
                    self._openai_client = openai.OpenAI(api_key=api_key)
                except Exception as e:
                    print(f"Warning: Failed to initialize OpenAI client: {e}")
                    self._openai_client = None
        return self._openai_client
    
    def _log_processing(self, process_type: str, patient_id: int = None, 
                       user_id: int = None, **kwargs) -> AIProcessingLog:
        """Log AI processing for audit trail"""
        return AIProcessingLog.objects.create(
            patient_id=patient_id,
            user_id=user_id,
            process_type=process_type,
            started_at=timezone.now(),
            **kwargs
        )
    
    def _call_openai(self, messages: List[Dict], model: str = None) -> AIResponse:
        """Make a call to OpenAI API with error handling"""
        start_time = timezone.now()
        model = model or self.default_model
        
        if not self.openai_client:
            return AIResponse(
                success=False,
                content="OpenAI client not available. Please configure OPENAI_API_KEY.",
                error="OpenAI client not initialized",
                processing_time_seconds=0,
                model_used=model,
                tokens_used=0
            )
        
        try:
            response = self.openai_client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                top_p=getattr(settings, 'AI_CONFIG', {}).get('TOP_P', 0.9)
            )
            
            processing_time = (timezone.now() - start_time).total_seconds()
            
            return AIResponse(
                success=True,
                content=response.choices[0].message.content,
                confidence=1.0,  # OpenAI doesn't return confidence directly
                model_used=model,
                tokens_used=response.usage.total_tokens,
                processing_time=processing_time
            )
            
        except Exception as e:
            processing_time = (timezone.now() - start_time).total_seconds()
            logger.error(f"OpenAI API call failed: {str(e)}")
            
            return AIResponse(
                success=False,
                content="",
                confidence=0.0,
                model_used=model,
                processing_time=processing_time,
                error_message=str(e)
            )


class ClinicalInsightGenerator(AIServiceManager):
    """Generate clinical insights from patient data"""
    
    def generate_patient_summary(self, patient_data: Dict) -> AIResponse:
        """Generate comprehensive patient summary with insights"""
        
        system_prompt = """You are a healthcare AI assistant specializing in clinical analysis. 
        Analyze the provided patient data and generate a comprehensive summary with actionable insights.
        Focus on:
        1. Current health status and trends
        2. Risk factors and potential concerns
        3. Medication interactions or issues
        4. Care gaps or documentation needs
        5. Recommendations for healthcare providers
        
        Format your response as structured JSON with the following sections:
        - summary: Brief overall summary
        - key_findings: List of important findings
        - risk_factors: Identified risk factors
        - recommendations: Actionable recommendations
        - urgency_level: immediate, within_24h, within_week, or routine
        """
        
        user_prompt = f"""Analyze this patient data:
        
        Patient Information: {json.dumps(patient_data, indent=2)}
        
        Provide insights focusing on clinical significance and actionable recommendations."""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        return self._call_openai(messages)
    
    def analyze_visit_notes(self, visit_notes: str, patient_context: Dict) -> AIResponse:
        """Analyze visit notes and extract insights"""
        
        system_prompt = """You are a clinical documentation AI assistant. 
        Analyze visit notes in the context of patient history and extract:
        1. Key clinical findings and changes
        2. Progress towards care goals
        3. New concerns or symptoms
        4. Medication adherence and effectiveness
        5. Documentation completeness for billing/compliance
        6. Suggestions for follow-up care
        
        Return structured analysis focusing on actionable insights."""
        
        user_prompt = f"""Visit Notes: {visit_notes}
        
        Patient Context: {json.dumps(patient_context, indent=2)}
        
        Analyze these notes and provide clinical insights."""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        return self._call_openai(messages)
    
    def identify_care_gaps(self, patient_data: Dict, oasis_data: Dict = None) -> AIResponse:
        """Identify gaps in patient care based on conditions and history"""
        
        system_prompt = """You are a healthcare quality assurance AI. 
        Analyze patient data to identify potential care gaps including:
        1. Missing assessments or screenings
        2. Overdue follow-ups or referrals
        3. Incomplete medication management
        4. Missed preventive care opportunities
        5. Documentation deficiencies
        6. OASIS compliance issues (if applicable)
        
        Prioritize gaps by clinical significance and regulatory requirements."""
        
        user_prompt = f"""Patient Data: {json.dumps(patient_data, indent=2)}
        
        OASIS Data: {json.dumps(oasis_data or {}, indent=2)}
        
        Identify care gaps and provide recommendations."""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        return self._call_openai(messages)


class RiskAssessmentEngine(AIServiceManager):
    """AI-powered risk assessment for various clinical outcomes"""
    
    def assess_fall_risk(self, patient_data: Dict) -> Tuple[float, Dict]:
        """Assess fall risk using AI analysis of patient factors"""
        
        # Extract relevant factors for fall risk
        factors = self._extract_fall_risk_factors(patient_data)
        
        system_prompt = """You are a clinical risk assessment AI specializing in fall risk prediction.
        Analyze the provided patient factors and return a fall risk assessment.
        
        Consider factors like:
        - Age and mobility status
        - Medications that increase fall risk
        - Previous falls history
        - Cognitive status
        - Environmental factors
        - Comorbidities
        
        Return a JSON response with:
        - risk_score: float between 0-1 (1 = highest risk)
        - risk_category: low, moderate, high, or critical
        - contributing_factors: list of factors increasing risk
        - protective_factors: list of factors reducing risk
        - recommendations: prevention strategies
        """
        
        user_prompt = f"Assess fall risk for patient with these factors: {json.dumps(factors, indent=2)}"
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        response = self._call_openai(messages)
        
        if response.success:
            try:
                risk_data = json.loads(response.content)
                return risk_data.get('risk_score', 0.0), risk_data
            except json.JSONDecodeError:
                logger.error("Failed to parse fall risk assessment response")
                return 0.0, {}
        
        return 0.0, {}
    
    def assess_readmission_risk(self, patient_data: Dict, recent_admissions: List) -> Tuple[float, Dict]:
        """Assess 30-day readmission risk"""
        
        system_prompt = """You are a readmission risk prediction AI. Analyze patient data to predict 
        30-day readmission risk based on clinical indicators, social determinants, and historical patterns.
        
        Key factors to consider:
        - Primary diagnosis and comorbidities
        - Previous admission patterns
        - Medication complexity
        - Social support and compliance
        - Discharge planning adequacy
        - Follow-up care arrangements
        
        Return structured risk assessment with score and recommendations."""
        
        context_data = {
            'patient_data': patient_data,
            'recent_admissions': recent_admissions
        }
        
        user_prompt = f"Assess readmission risk: {json.dumps(context_data, indent=2)}"
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        response = self._call_openai(messages)
        
        if response.success:
            try:
                risk_data = json.loads(response.content)
                return risk_data.get('risk_score', 0.0), risk_data
            except json.JSONDecodeError:
                return 0.0, {}
        
        return 0.0, {}
    
    def _extract_fall_risk_factors(self, patient_data: Dict) -> Dict:
        """Extract relevant factors for fall risk assessment"""
        factors = {}
        
        # Age
        if 'age' in patient_data:
            factors['age'] = patient_data['age']
        
        # Medications
        if 'medications' in patient_data:
            fall_risk_meds = []
            for med in patient_data['medications']:
                # Check for fall-risk medications
                med_name = med.get('name', '').lower()
                if any(risky in med_name for risky in ['sedative', 'hypnotic', 'antipsychotic', 'benzodiazepine']):
                    fall_risk_meds.append(med)
            factors['fall_risk_medications'] = fall_risk_meds
        
        # Mobility and functional status
        if 'functional_status' in patient_data:
            factors['mobility'] = patient_data['functional_status']
        
        # History of falls
        if 'history' in patient_data:
            factors['fall_history'] = patient_data['history'].get('falls', [])
        
        return factors


class TrendAnalyzer(AIServiceManager):
    """Analyze trends in patient data over time"""
    
    def analyze_vital_trends(self, patient_id: int, metric_name: str, 
                           data_points: List[Dict], days: int = 30) -> Dict:
        """Analyze trends in vital signs or other metrics"""
        
        if len(data_points) < 3:
            return {"error": "Insufficient data points for trend analysis"}
        
        # Calculate basic trend statistics
        values = [point['value'] for point in data_points]
        timestamps = [point['timestamp'] for point in data_points]
        
        # Simple trend calculation (could be enhanced with more sophisticated methods)
        trend_direction = self._calculate_trend_direction(values)
        trend_strength = self._calculate_trend_strength(values)
        
        # Get AI interpretation
        system_prompt = f"""You are a clinical data analyst AI. Analyze the trend in {metric_name} 
        over the past {days} days and provide clinical interpretation.
        
        Consider:
        - Clinical significance of the trend
        - Normal ranges for this metric
        - Potential causes for changes
        - Recommendations for monitoring or intervention
        
        Return analysis focusing on clinical implications."""
        
        trend_data = {
            'metric': metric_name,
            'data_points': data_points,
            'trend_direction': trend_direction,
            'trend_strength': trend_strength,
            'analysis_period': f"{days} days"
        }
        
        user_prompt = f"Analyze this clinical trend: {json.dumps(trend_data, indent=2)}"
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        response = self._call_openai(messages)
        
        result = {
            'trend_direction': trend_direction,
            'trend_strength': trend_strength,
            'data_points_count': len(data_points),
            'analysis_period_days': days
        }
        
        if response.success:
            result['ai_interpretation'] = response.content
            result['clinical_significance'] = self._extract_clinical_significance(response.content)
        
        return result
    
    def _calculate_trend_direction(self, values: List[float]) -> str:
        """Calculate basic trend direction"""
        if len(values) < 2:
            return 'stable'
        
        # Simple linear trend
        first_half = sum(values[:len(values)//2]) / (len(values)//2)
        second_half = sum(values[len(values)//2:]) / (len(values) - len(values)//2)
        
        diff_threshold = 0.1  # 10% change threshold
        relative_change = abs(second_half - first_half) / first_half
        
        if relative_change < diff_threshold:
            return 'stable'
        elif second_half > first_half:
            return 'improving'
        else:
            return 'declining'
    
    def _calculate_trend_strength(self, values: List[float]) -> float:
        """Calculate trend strength (0-1 scale)"""
        if len(values) < 3:
            return 0.0
        
        # Calculate coefficient of variation as a measure of stability
        import statistics
        mean_val = statistics.mean(values)
        if mean_val == 0:
            return 0.0
        
        std_dev = statistics.stdev(values)
        cv = std_dev / mean_val
        
        # Convert to trend strength (inverse of volatility)
        return max(0.0, min(1.0, 1.0 - cv))
    
    def _extract_clinical_significance(self, ai_response: str) -> str:
        """Extract clinical significance from AI response"""
        # Simple extraction - could be enhanced with more sophisticated NLP
        if 'significant' in ai_response.lower() or 'concerning' in ai_response.lower():
            return 'high'
        elif 'moderate' in ai_response.lower() or 'notable' in ai_response.lower():
            return 'moderate'
        else:
            return 'low'


class DocumentAnalyzer(AIServiceManager):
    """Analyze clinical documents and extract structured data"""
    
    def extract_clinical_data(self, document_text: str, document_type: str) -> Dict:
        """Extract structured clinical data from documents"""
        
        system_prompt = f"""You are a clinical document analysis AI. Extract structured data from 
        {document_type} documents. Focus on:
        
        1. Patient demographics
        2. Diagnoses and conditions
        3. Medications and dosages
        4. Vital signs and measurements
        5. Procedures and treatments
        6. Assessment findings
        7. Plan of care
        
        Return structured JSON data with extracted information clearly categorized."""
        
        user_prompt = f"Extract clinical data from this {document_type}:\n\n{document_text}"
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        response = self._call_openai(messages)
        
        if response.success:
            try:
                return json.loads(response.content)
            except json.JSONDecodeError:
                # Return raw text if JSON parsing fails
                return {'raw_analysis': response.content}
        
        return {'error': 'Failed to analyze document'}
    
    def generate_provider_communication(self, patient_data: Dict, 
                                      concerns: List[str]) -> AIResponse:
        """Generate communication for primary care providers"""
        
        system_prompt = """You are a healthcare communication AI assistant. Generate clear, 
        professional communication for primary care providers based on patient data and concerns.
        
        Include:
        1. Brief patient summary
        2. Specific concerns or changes
        3. Current status and trends
        4. Recommendations or questions
        5. Urgency level
        
        Use professional medical terminology while being concise and actionable."""
        
        communication_data = {
            'patient_summary': patient_data,
            'specific_concerns': concerns,
            'date_of_communication': datetime.now().isoformat()
        }
        
        user_prompt = f"""Generate provider communication for:
        {json.dumps(communication_data, indent=2)}
        
        Format as professional clinical communication."""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        return self._call_openai(messages)


# Initialize AI services
clinical_insight_generator = ClinicalInsightGenerator()
risk_assessment_engine = RiskAssessmentEngine()
trend_analyzer = TrendAnalyzer()
document_analyzer = DocumentAnalyzer()
