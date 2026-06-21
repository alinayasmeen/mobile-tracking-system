"""
Automated IMEI Matching and Report State Evaluation Agent

This sub-agent is a production-grade intelligence subagent designed to handle automated IMEI matching 
and report state evaluation within a mobile tracking and snatched-phone prevention system.

Its primary responsibility is to analyze phone-related events (such as lost/snatched reports, 
retailer purchase registrations, and received-phone submissions) and automatically determine 
whether an IMEI match exists between citizen reports and retailer records.

The sub-agent is invoked by a parent/orchestrator agent whenever:
- A citizen reports a phone as lost or snatched
- A retailer registers a phone purchase or submits a received phone
- An admin requests verification or system-wide match analysis

Upon invocation, the sub-agent receives structured input containing IMEI, phone metadata, 
report status, and contextual role information. It evaluates this data against predefined 
business rules, including:
- Exact IMEI matching
- Report state transitions (PENDING → VERIFIED → MATCHED)
- Conflict or duplication detection
- Eligibility for automatic flagging

The sub-agent returns a structured JSON response indicating:
- Whether a match was found
- The confidence and reason for the match
- Recommended next actions (e.g., flag report, notify admin, lock ownership transfer)

This sub-agent is not user-facing and does not perform authentication, authorization, 
or direct database mutations. All security, RBAC, and persistence responsibilities 
are handled by the parent agent or API layer.

Key characteristics:
- Single-responsibility, event-driven design
- Deterministic and explainable decision-making
- Structured input/output suitable for audit logs
- Async and scalable execution
- Designed for integration with FastAPI and SQL-based backends
- Safe for production use in law-enforcement-adjacent systems
"""

from openai_imei_agent_client import OpenAIIMEIAgentClient
import sys
import os

# Add the parent directory to the path to import from agents
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai_agents.agent_models import EventType, AgentInput, AgentResponse, MatchResult
from typing import List


class IMEIMatchingAgent:
    """
    Interface to the OpenAI-based intelligence subagent for automated IMEI matching and report state evaluation.
    
    This class acts as a bridge between the main application and the OpenAI agent service
    running as a separate process.
    
    Key characteristics:
    - Single-responsibility, event-driven design
    - Deterministic and explainable decision-making
    - Structured input/output suitable for audit logs
    - Async and scalable execution
    - Designed for integration with FastAPI and SQL-based backends
    - Safe for production use in law-enforcement-adjacent systems
    """
    
    def __init__(self, agent_service_url: str = "http://localhost:8001"):
        self.client = OpenAIIMEIAgentClient(base_url=agent_service_url)
        
    def process_event(self, agent_input: AgentInput) -> AgentResponse:
        """
        Process an incoming event and evaluate for IMEI matches.
        
        Args:
            agent_input: Structured input containing event details
            
        Returns:
            AgentResponse with match results and recommendations
        """
        return self.client.process_event(agent_input)
    
    def run_system_wide_analysis(self) -> AgentResponse:
        """
        Perform a system-wide analysis to find all possible IMEI matches.
        
        Returns:
            AgentResponse with all matches found in the system
        """
        return self.client.run_system_wide_analysis()


# Example usage function
def example_usage():
    """
    Example of how to use the IMEI matching agent
    """
    agent = IMEIMatchingAgent()
    
    # Example 1: Processing a new report
    agent_input = AgentInput(
        event_type=EventType.REPORT_LOST_SNATCHED,
        imei="123456789012345",
        phone_metadata={
            "brand": "Samsung",
            "model": "Galaxy S21"
        },
        report_id=1,
        report_status="PENDING",
        user_role="citizen"
    )
    
    response = agent.process_event(agent_input)
    print(response.json(indent=2))


if __name__ == "__main__":
    example_usage()