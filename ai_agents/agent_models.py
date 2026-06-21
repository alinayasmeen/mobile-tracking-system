"""
Shared models for the IMEI Matching Agent system
"""

from typing import Dict, List, Optional
from pydantic import BaseModel
from enum import Enum


class EventType(str, Enum):
    """Types of events that trigger the agent"""
    REPORT_LOST_SNATCHED = "report_lost_snatched"
    RETAILER_PURCHASE = "retailer_purchase"
    RECEIVED_PHONE = "received_phone"
    SYSTEM_ANALYSIS = "system_analysis"


class AgentInput(BaseModel):
    """Structured input for the IMEI matching agent"""
    event_type: EventType
    imei: str
    phone_metadata: Optional[Dict] = {}
    report_id: Optional[int] = None
    purchase_id: Optional[int] = None
    report_status: Optional[str] = None
    user_role: Optional[str] = None  # citizen, retailer, admin


class MatchResult(BaseModel):
    """Result of a single match evaluation"""
    imei: str
    match_found: bool
    confidence_score: float  # 0.0 to 1.0
    reason: str
    matched_report_id: Optional[int] = None
    matched_purchase_id: Optional[int] = None
    matched_phone_id: Optional[int] = None


class AgentResponse(BaseModel):
    """Structured response from the IMEI matching agent"""
    success: bool
    message: str
    matches: List[MatchResult]
    recommended_actions: List[str]