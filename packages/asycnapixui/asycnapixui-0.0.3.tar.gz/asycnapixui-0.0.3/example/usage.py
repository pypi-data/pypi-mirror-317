import asyncio
from datetime import datetime, timedelta
from logging import DEBUG, getLogger, basicConfig
from uuid import uuid4

from src.asycnapixui import Api
from src.asycnapixui import Client, ExpiryTime


async def main():
    async with Api(url="https://example.com:port/path/", login="admin", password="admin", token="") as api:
        """
        create api session
        """

        clients = []
        emails = ['Petya', 'Vasya', 'Egor']

        """get inbound by id"""
        inbound = await api.get_inbound(1)

        """create clients list"""
        for email in emails:
            key = str(uuid4())
            clients.append(Client(id=key, email=email, subId=key))

        """add clients to inbound """
        await api.post_add_client_inbound(clients, inbound.id)

        """
        enable clients in inbound 
        and add date to end = now + 10 days
        """
        for client in clients:
            client.enable = True
            client.expiryTime = ExpiryTime(date=datetime.now() + timedelta(days=10)).expiryTime
            await api.post_update_client(client, inbound.id, client.id)


"""
logs with information about responses
"""

logger = getLogger()
basicConfig(level=DEBUG, format='%(asctime)s : %(levelname)s:%(name)s : %(funcName)s:%(message)s')


if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())