from spade.agent import Agent
from pyjabber.server import Server


async def test_create_agent():
    server = Server(host="localhost", client_port=5222)
    server.database_purge = True
    server.database_path = "."
    agent = Agent("test@localhost", "test")

    await server.start()
    await agent.start()

    assert agent.is_alive()
