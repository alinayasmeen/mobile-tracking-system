"""
HTTP Client for OpenAI IMEI Matching Agent Service

This client allows the main application to communicate with the OpenAI agent service
running as a separate process.
"""

import requests
import sys
import os

# Add the parent directory to the path to import from agents
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai_agents.agent_models import AgentInput, EventType, AgentResponse, MatchResult  # Import from the models file


class OpenAIIMEIAgentClient:
    """
    HTTP client for communicating with the OpenAI IMEI Matching Agent Service
    """
    
    def __init__(self, base_url: str = "http://localhost:8001"):
        self.base_url = base_url
    
    def process_event(self, agent_input: AgentInput) -> AgentResponse:
        """
        Send an event to the agent service for processing
        
        Args:
            agent_input: The input data for the agent
            
        Returns:
            AgentResponse from the agent service
        """
        url = f"{self.base_url}/process-event"
        
        # Convert the input to a dictionary
        input_dict = {
            "event_type": agent_input.event_type.value,
            "imei": agent_input.imei,
            "phone_metadata": agent_input.phone_metadata,
            "report_id": agent_input.report_id,
            "purchase_id": agent_input.purchase_id,
            "report_status": agent_input.report_status,
            "user_role": agent_input.user_role
        }
        
        try:
            response = requests.post(url, json=input_dict)
            response.raise_for_status()

            # Convert response to AgentResponse object
            data = response.json()
            matches = data.get("matches", [])
            recommended_actions = data.get("recommended_actions", [])

            # Create MatchResult objects from the response
            match_objects = []
            for match_data in matches:
                match_obj = MatchResult(**match_data)
                match_objects.append(match_obj)

            return AgentResponse(
                success=data["success"],
                message=data["message"],
                matches=match_objects,
                recommended_actions=recommended_actions
            )
        except requests.exceptions.RequestException as e:
            # Return an error response if the request fails
            return AgentResponse(
                success=False,
                message=f"Error communicating with agent service: {str(e)}",
                matches=[],
                recommended_actions=[]
            )
    
    def run_system_wide_analysis(self) -> AgentResponse:
        """
        Run a system-wide analysis using the agent service
        
        Returns:
            AgentResponse from the agent service
        """
        url = f"{self.base_url}/system-analysis"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            
            # Convert response to AgentResponse object
            data = response.json()
            matches = data.get("matches", [])
            recommended_actions = data.get("recommended_actions", [])
            
            # Create MatchResult objects from the response
            match_objects = []
            for match_data in matches:
                match_obj = MatchResult(**match_data)
                match_objects.append(match_obj)
            
            return AgentResponse(
                success=data["success"],
                message=data["message"],
                matches=match_objects,
                recommended_actions=recommended_actions
            )
        except requests.exceptions.RequestException as e:
            # Return an error response if the request fails
            return AgentResponse(
                success=False,
                message=f"Error communicating with agent service: {str(e)}",
                matches=[],
                recommended_actions=[]
            )