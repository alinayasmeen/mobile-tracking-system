"""
FastAPI Application for OpenAI IMEI Matching Agent Service

This service runs separately from the main application and handles
automated IMEI matching and report state evaluation using OpenAI agents.
"""

import sys, os
# Ensure the repository root (the directory that contains the "agents" package) is on the import path.
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from fastapi import FastAPI, HTTPException
from typing import List
import asyncio
import os
from dotenv import load_dotenv
import uvicorn

# Load environment variables
load_dotenv()

# Import the agent service
from openai_imei_agent_service import OpenAIIMEIMatchingAgentService
from agent_models import AgentInput, AgentResponse


app = FastAPI(title="OpenAI IMEI Matching Agent Service", version="1.0.0")


@app.on_event("startup")
async def startup_event():
    """Initialize the agent service on startup"""
    app.agent_service = OpenAIIMEIMatchingAgentService()


@app.post("/process-event")
async def process_event(agent_input: AgentInput):
    """Process an incoming event and evaluate for IMEI matches"""
    try:
        response = await app.agent_service.process_event(agent_input)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/system-analysis")
async def system_analysis():
    """Perform a system-wide analysis to find all possible IMEI matches"""
    try:
        response = await app.agent_service.run_system_wide_analysis()
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
async def root():
    return {
        "message": "OpenAI IMEI Matching Agent Service",
        "version": "1.0.0",
        "docs": "/docs"
    }


if __name__ == "__main__":
  
    uvicorn.run(app, host="0.0.0.0", port=8001)