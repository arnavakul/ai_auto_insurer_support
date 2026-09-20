import asyncio
import json

from langchain.tools import tool

from a2a.client import create_client,ClientConfig
from a2a.helpers import new_text_message
from a2a.types import Role, SendMessageRequest

COST_AGENT_URL = "http://127.0.0.1:9004/"

@tool
def cost_estimation_agent_tool(user_input: str) -> str: 
    
    """
        Estimate the damage of the vehicle and give the cost of repairing.
    """
    
    return asyncio.run(
        _call_cost_estimation_agent(user_input)
    )

async def _call_cost_estimation_agent(user_input: str) -> str:
    
    #created the A2A client
    client = await create_client(
        COST_AGENT_URL,
        client_config=ClientConfig(streaming=False),
    )
    
    try: 
        
        message = new_text_message(
            text = user_input,
            role = Role.ROLE_USER
        )
        
        request = SendMessageRequest(
            message=message
        )
        
        responses = []
        
        async for response in client.send_message(request):
            response.append(response)
        
        return json.dumps(
            [str(response) for response in responses],
            default=str,
        )
    finally: 
        await client.close()