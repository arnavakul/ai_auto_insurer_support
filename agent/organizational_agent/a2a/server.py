import uvicorn
from starlette.applications import Starlette
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.routes import (
    create_agent_card_routes,
    create_jsonrpc_routes
)

from a2a.server.tasks import InMemoryTaskStore

from .agent_card import organization_agent_card
from .agent_executor import OrganizationAgentExecutor

def main(): 
    
    agent_card = organization_agent_card() #creates agent card
    #this ultimately connects A2A protocol to request handler to executor
    request_handler = DefaultRequestHandler(
        agent_executor=OrganizationAgentExecutor(),  #creates : A2A → Your agent adapter
        task_store=InMemoryTaskStore(),
        agent_card=agent_card, 
    )
    
    routes = []
    
    routes.extend(
        create_agent_card_routes(agent_card)
    )
    
    routes.extend(
        create_jsonrpc_routes(
            request_handler, 
            "/",
        )
    )
    
    app = Starlette(
        routes=routes
    )
    
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=9003
    )

if __name__ == "__main__":
    main()