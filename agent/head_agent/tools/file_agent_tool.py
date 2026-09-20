import asyncio
import json

from langchain.tools import tool

from a2a.client import create_client,ClientConfig
from a2a.helpers import new_text_message
from a2a.types import Role, SendMessageRequest

FILE_AGENT_URL = "http://127.0.0.1:9001/"

@tool
def file_agent_tool(user_input: str) -> str: 
    
    """
    Send a document-processing request to the File Agent.

    The File Agent extracts information from claim documents
    such as FIRs, vehicle damage reports, repair estimates,
    and damage photos.
    """
    
    return asyncio.run(
        _call_file_agent(user_input)
    )

async def _call_file_agent(user_input: str) -> str:
    
    #created the A2A client
    client = await create_client(
        FILE_AGENT_URL,
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
            [list(response) for response in responses],
            default=list,
        )
    finally: 
        await client.close()