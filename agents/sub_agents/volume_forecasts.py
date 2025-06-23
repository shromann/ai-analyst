from google.adk.agents import Agent
import os

from ..tools import DataToolset

vf_path = os.path.join(
    os.path.dirname(__file__),
    '..', 'database', 'volume_forecasts'
)

vf = DataToolset(vf_path)


volume_forecasts_agent = Agent(
    name = vf.agent_name,
    model = 'gemini-2.0-flash',
    description = vf.description,
    instruction = vf.instruction,
    tools=[vf.query_tool, vf.plot_tool, vf.forecast_tool],
    output_key='volume_forecasts_out'
)
