"""
OpenAI Agent Service for Automated IMEI Matching and Report State Evaluation

This service runs as a separate process and handles automated IMEI matching 
and report state evaluation within a mobile tracking and snatched-phone prevention system.

Its primary responsibility is to analyze phone-related events (such as lost/snatched reports, 
retailer purchase registrations, and received-phone submissions) and automatically determine 
whether an IMEI match exists between citizen reports and retailer records.
"""

import os
import asyncio
from typing import Dict, List, Optional
from enum import Enum
from dotenv import load_dotenv
from pydantic import BaseModel

from agents import (
    Agent,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    RunConfig,
)


load_dotenv()

# Initialize OpenAI client (using Gemini via OpenAI-compatible API)
client = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    openai_client=client,
    model="gemini-2.0-flash",
)

config = RunConfig(model=model)

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


class OpenAIIMEIMatchingAgentService:
    """
    OpenAI-based intelligence agent service for automated IMEI matching and report state evaluation.
    
    This service runs separately from the main application and communicates via HTTP/gRPC.
    
    Key characteristics:
    - Single-responsibility, event-driven design
    - Deterministic and explainable decision-making using OpenAI
    - Structured input/output suitable for audit logs
    - Async and scalable execution
    - Designed for integration with external systems
    - Safe for production use in law-enforcement-adjacent systems
    """
    
    def __init__(self):
        self.agent = Agent(
            name="IMEIMatchingAgent",
            instructions="""
            You are an expert in mobile phone tracking and IMEI matching. 
            Analyze the provided data and determine if there are any matches between reported lost/snatched phones and retailer purchases.
            Apply business rules for matching, including checking report statuses and determining confidence scores.
            Respond with structured JSON containing match results and recommendations.
            """,
            model=model,
        )
        
    async def process_event(self, agent_input: AgentInput) -> AgentResponse:
        """
        Process an incoming event and evaluate for IMEI matches using OpenAI.
        
        Args:
            agent_input: Structured input containing event details
            
        Returns:
            AgentResponse with match results and recommendations
        """
        try:
            # Prepare the prompt for the agent
            prompt = self._create_prompt(agent_input)
            
            # Run the agent
            result = await self.agent.run(
                prompt,
                run_config=config,
            )
            
            # Parse the response (assuming it returns JSON)
            import json
            try:
                ai_response = json.loads(result.output_text)
            except json.JSONDecodeError:
                # If JSON parsing fails, return an error response
                return AgentResponse(
                    success=False,
                    message=f"Invalid JSON response from agent: {result.output_text}",
                    matches=[],
                    recommended_actions=[]
                )
            
            # Convert to our response format
            matches = []
            for match_data in ai_response.get("matches", []):
                match = MatchResult(**match_data)
                matches.append(match)
            
            recommended_actions = ai_response.get("recommended_actions", [])
            
            return AgentResponse(
                success=True,
                message=ai_response.get("message", f"Successfully processed {agent_input.event_type} event for IMEI {agent_input.imei}"),
                matches=matches,
                recommended_actions=recommended_actions
            )
            
        except Exception as e:
            return AgentResponse(
                success=False,
                message=f"Error processing event with OpenAI agent: {str(e)}",
                matches=[],
                recommended_actions=[]
            )
    
    def _create_prompt(self, agent_input: AgentInput) -> str:
        """
        Create a prompt for the OpenAI agent based on the agent input.
        
        Args:
            agent_input: The input data for the agent
            
        Returns:
            Formatted prompt string
        """
        prompt = f"""
        Analyze the following mobile tracking event and determine if there are any IMEI matches:

        Event Type: {agent_input.event_type}
        IMEI: {agent_input.imei}
        Phone Metadata: {str(agent_input.phone_metadata)}
        Report ID: {agent_input.report_id}
        Purchase ID: {agent_input.purchase_id}
        Report Status: {agent_input.report_status}
        User Role: {agent_input.user_role}

        Business Rules:
        1. An IMEI match occurs when the same IMEI appears in both a lost/snatched report and a retailer purchase
        2. Reports with status PENDING or VERIFIED are eligible for matching
        3. Reports with status MATCHED or CLEARED are not eligible for additional matching
        4. The confidence score should be high (0.9-1.0) for exact IMEI matches
        5. Recommended actions should include flagging reports, notifying admins, or locking transfers

        Please respond with a JSON object in the following format:
        {{
          "message": "Success message",
          "matches": [
            {{
              "imei": "string",
              "match_found": true/false,
              "confidence_score": 0.0-1.0,
              "reason": "explanation of match or no match",
              "matched_report_id": integer or null,
              "matched_purchase_id": integer or null,
              "matched_phone_id": integer or null
            }}
          ],
          "recommended_actions": ["action1", "action2", ...]
        }}
        """
        return prompt
    
    async def run_system_wide_analysis(self) -> AgentResponse:
        """
        Perform a system-wide analysis to find all possible IMEI matches using OpenAI.
        
        Returns:
            AgentResponse with all matches found in the system
        """
        prompt = """
        Perform a comprehensive analysis of the entire mobile tracking database to identify all possible IMEI matches between:
        1. Lost/snatched reports and retailer purchases
        2. Flag any suspicious patterns or anomalies
        3. Provide recommendations for improving the tracking system
        
        Focus on identifying duplicate IMEIs, frequent sellers, and other patterns that might indicate stolen phone trafficking.
        
        Respond in the same JSON format as before.
        """
        
        try:
            result = await self.agent.run(
                prompt,
                run_config=config,
            )
            
            import json
            try:
                ai_response = json.loads(result.output_text)
            except json.JSONDecodeError:
                # If JSON parsing fails, return an error response
                return AgentResponse(
                    success=False,
                    message=f"Invalid JSON response from agent: {result.output_text}",
                    matches=[],
                    recommended_actions=[]
                )
            
            matches = []
            for match_data in ai_response.get("matches", []):
                match = MatchResult(**match_data)
                matches.append(match)
            
            recommended_actions = ai_response.get("recommended_actions", [])
            
            return AgentResponse(
                success=True,
                message=ai_response.get("message", "System-wide analysis completed"),
                matches=matches,
                recommended_actions=recommended_actions
            )
            
        except Exception as e:
            return AgentResponse(
                success=False,
                message=f"Error performing system-wide analysis with OpenAI agent: {str(e)}",
                matches=[],
                recommended_actions=[]
            )


# Example usage
async def example_usage():
    agent_service = OpenAIIMEIMatchingAgentService()
    
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
    
    response = await agent_service.process_event(agent_input)
    print(response.json(indent=2))


if __name__ == "__main__":
    asyncio.run(example_usage())