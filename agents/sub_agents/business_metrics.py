from google.adk.agents import Agent
import os

from ..tools import DataToolset

bm_path = os.path.join(
    os.path.dirname(__file__), 
    '..', 'database', 'business_metrics'
)

bm = DataToolset(bm_path)


business_metrics_agent = Agent(
    name = bm.agent_name,
    model = 'gemini-2.0-flash',
    description = bm.description,
    instruction = bm.instruction,
    tools=[bm.query_tool, bm.plot_tool, bm.forecast_tool],
    output_key='business_metrics_out'
)

