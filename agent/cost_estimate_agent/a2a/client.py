import asyncio

from a2a.client import create_client, ClientConfig
from a2a.helpers import new_text_message
from a2a.types import Role, SendMessageRequest


async def main():
    
    client_config = ClientConfig(
        streaming=False
    )

    client = await create_client(
        "http://127.0.0.1:9004/",
        client_config=client_config
    )

    message = new_text_message(
        text=(
            "Estimate the repair cost for a vehicle with front bumper "
            "and left fender damage. The vehicle is a mid-size sedan "
            "located in Mumbai. Provide an estimated repair cost range."
        ),
        role=Role.ROLE_USER,
    )
    
    request = SendMessageRequest(
        message=message
    )
    
    print("Sending message to Cost Estimation Agent ... \n")

    async for response in client.send_message(request):
        print("Response: ")
        print(response)
    
    await client.close()

if __name__ == "__main__":
    asyncio.run(main())