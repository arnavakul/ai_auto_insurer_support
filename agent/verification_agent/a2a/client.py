import asyncio

from a2a.client import create_client, ClientConfig
from a2a.helpers import new_text_message
from a2a.types import Role, SendMessageRequest


async def main():
    
    client_config = ClientConfig(
        streaming=False
    )

    client = await create_client(
        "http://127.0.0.1:9002/",
        client_config=client_config
    )

    message = new_text_message(
        text="Compare the incoming request from the user to documents attached. ",
        role=Role.ROLE_USER,
    )
    
    request = SendMessageRequest(
        message=message
    )
    
    print("Sending message to Verification Agent ... \n")

    async for response in client.send_message(request):
        print("Response: ")
        print(response)
    
    await client.close()

if __name__ == "__main__":
    asyncio.run(main())