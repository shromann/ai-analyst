from google.adk.agents import Agent
from datetime import datetime

from .sub_agents import (
    business_metrics_agent,
    volume_forecasts_agent
)

root_agent = Agent(
    name = 'ai_analyst',
    model = 'gemini-2.0-flash',
    global_instruction=f"""
    <current_datetime>{datetime.now()}<current_datetime>
    You must use the current datetime to infer the time 
    period value.""",
    description = """You are a helpful assistant
    that has sub agents to get volume forecasts
    data and business metrics data.""",
    instruction = """
    <persona>You are a helpful ai analyst assistant</persona>
    <task>Use the sub agents to get volume forecasts data and business metrics data</task>
    <context>When the user asks 'you' to do something, they are refering to you and all sub agents</context>
    """,
    sub_agents=[
        volume_forecasts_agent,
        business_metrics_agent
    ]
)


