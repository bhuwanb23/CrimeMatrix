from app.models.user import User
from app.models.case import Case
from app.models.fir import FIR
from app.models.suspect import Suspect
from app.models.evidence import Evidence
from app.models.investigation import Investigation
from app.models.alert import Alert
from app.models.case_embedding import CaseEmbedding
from app.models.case_similarity import CaseSimilarity
from app.models.crime_pattern import CrimePattern
from app.models.pattern_occurrence import PatternOccurrence
from app.models.pattern_cluster import PatternCluster
from app.models.crime_statistic import CrimeStatistic
from app.models.trend_snapshot import TrendSnapshot
from app.models.crime_hotspot import CrimeHotspot
from app.models.location_cluster import LocationCluster
from app.models.behavior_profile import BehaviorProfile
from app.models.behavior_feature import BehaviorFeature
from app.models.repeat_offender import RepeatOffender
from app.models.offender_score import OffenderScore
from app.models.mo_profile import MOProfile
from app.models.mo_embedding import MOEmbedding
from app.models.mo_similarity_record import MOSimilarityRecord
from app.models.crime_prediction import CrimePrediction
from app.models.prediction_model import PredictionModelRecord
from app.models.prediction_result import PredictionResult
from app.models.early_warning_alert import EarlyWarningAlert
from app.models.alert_rule import AlertRule
from app.models.alert_event import AlertEvent
from app.models.suspect_risk_score import SuspectRiskScore
from app.models.risk_score_history import RiskScoreHistory
from app.models.risk_factor import RiskFactor
from app.models.crime_forecast_record import CrimeForecastRecord
from app.models.forecast_snapshot import ForecastSnapshot
from app.models.case_priority import CasePriority
from app.models.priority_history_record import PriorityHistoryRecord
from app.models.priority_explanation import PriorityExplanation
from app.models.prediction_explanation_record import PredictionExplanationRecord
from app.models.prediction_source import PredictionSource
from app.models.model_metric import ModelMetric
from app.models.prediction_feedback_record import PredictionFeedbackRecord
from app.models.evaluation_result import EvaluationResult
from app.models.intelligence_event import IntelligenceEvent
from app.models.event_queue_record import EventQueueRecord
from app.models.processed_event import ProcessedEvent
from app.models.fir_suggestion import FIRSuggestion
from app.models.fir_analysis_history_record import FIRAnalysisHistoryRecord
from app.models.cross_district_match import CrossDistrictMatch
from app.models.match_history_record import MatchHistoryRecord

# Core crime data models
from app.models.crime import Crime
from app.models.crimetype import CrimeType
from app.models.criminal import Criminal
from app.models.person import Person
from app.models.victim import Victim
from app.models.witness import Witness
from app.models.officer import Officer
from app.models.station import Station
from app.models.district import District
from app.models.vehicle import Vehicle
from app.models.phone import Phone
from app.models.location import Location

# Investigation models
from app.models.attachment import Attachment
from app.models.bookmark import Bookmark
from app.models.case_link import CaseLink
from app.models.case_status_log import CaseStatusLog
from app.models.note import Note
from app.models.timeline_event import TimelineEvent
from app.models.report import Report

# Audit & monitoring models
from app.models.audit import AuditLog, AIDecision, APILog
from app.models.chat import ChatSession, ChatMessage, ConversationMemory
from app.models.feedback import Feedback
from app.models.notification import Notification

# Graph & identity models
from app.models.graph_meta import GraphNode, GraphEdge
from app.models.identity import IdentityGroup, IdentityMatch
from app.models.search import SavedSearch, SearchHistory

# Prediction models
from app.models.prediction import Prediction, RiskScore

# Officer intel models
from app.models.officer_intel import CaseAssignment, Recommendation

__all__ = [
    # Core
    "User", "Case", "FIR", "Suspect", "Evidence", "Investigation", "Alert",
    # Crime data
    "Crime", "CrimeType", "Criminal", "Person", "Victim", "Witness",
    "Officer", "Station", "District", "Vehicle", "Phone", "Location",
    # Investigation
    "Attachment", "Bookmark", "CaseLink", "CaseStatusLog", "Note",
    "TimelineEvent", "Report",
    # Intelligence
    "CaseEmbedding", "CaseSimilarity", "CrimePattern", "PatternOccurrence",
    "PatternCluster", "CrimeStatistic", "TrendSnapshot", "CrimeHotspot",
    "LocationCluster", "BehaviorProfile", "BehaviorFeature",
    "RepeatOffender", "OffenderScore", "MOProfile", "MOEmbedding",
    "MOSimilarityRecord",
    # Prediction
    "CrimePrediction", "PredictionModelRecord", "PredictionResult",
    "Prediction", "PredictionExplanationRecord", "PredictionSource",
    "CrimeForecastRecord", "ForecastSnapshot", "ModelMetric",
    "PredictionFeedbackRecord", "EvaluationResult",
    # Risk & priority
    "SuspectRiskScore", "RiskScoreHistory", "RiskFactor",
    "CasePriority", "PriorityHistoryRecord", "PriorityExplanation",
    # Alerts
    "EarlyWarningAlert", "AlertRule", "AlertEvent",
    # Audit & monitoring
    "AuditLog", "AIDecision", "APILog", "ChatSession", "ChatMessage",
    "ConversationMemory", "Feedback", "Notification",
    # Graph & identity
    "GraphNode", "GraphEdge", "IdentityGroup", "IdentityMatch",
    "SavedSearch", "SearchHistory",
    # Officer intel
    "CaseAssignment", "Recommendation",
]
