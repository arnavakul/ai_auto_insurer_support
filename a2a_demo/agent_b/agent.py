class MyAgent:

    async def invoke(self, message: str) -> str:
        return f"Agent B received: {message}"