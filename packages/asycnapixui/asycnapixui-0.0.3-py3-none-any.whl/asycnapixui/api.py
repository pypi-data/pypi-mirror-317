import json

from typing import Any
from aiohttp import ClientSession

from asycnapixui.log import logger, info
from asycnapixui.models import Inbound, ClientTraffic, Client


class Api:
    _headers = { 'Accept': 'application/json' }
    def __init__(self, url: str, login: str, password: str, token: str = None):
        """
        :param url:
        :param login:
        :param password:
        """
        self.url = url
        self.auth = {"username" : login,
                     "password" : password,
                     "loginSecret" : token if token else ""
                     }
        self.session = ClientSession(base_url=self.url)
        logger.info('Session started')

    async def __aenter__(self):
        resp = await self.session.post('login', data=self.auth)
        logger.info('Logining in x-ui panel')
        resp_json = await resp.json()
        logger.debug('Response %s', resp_json)
        if resp_json['success']:
            logger.info('Success')
        else:
            logger.info(resp_json['msg'])
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if not self.session.closed:
            await self.session.close()
            logger.info('Session closed')
        return False

    async def close(self):
        if not self.session.closed:
            await self.session.close()
            logger.info('Session closed')

    @info
    async def post_login(self):
        logger.info('Logining in x-ui panel')
        async with self.session.post('login', data=self.auth) as resp:
            resp_json = await resp.json()
            logger.debug('Response %s', resp_json)
            return resp_json

    async def get_inbounds(self) -> list[Inbound]:
        async with self.session.get('panel/api/inbounds/list') as resp:
            inbounds = []
            resp_json = await resp.json()
            logger.debug('Response %s', resp_json)
            for i in resp_json['obj']:
                inbounds.append(Inbound(**i))
            return inbounds

    async def get_inbound(self, inboundId: int) -> Inbound:
        async with self.session.get(f'panel/api/inbounds/get/{inboundId}') as resp:
            resp_json = await resp.json()
            logger.debug('Response %s', resp_json)
            return Inbound(**resp_json['obj'])

    async def get_client_traffics(self, email: str = None, uuid: str = None):
        if email:
            async with self.session.get(f'panel/api/inbounds/getClientTraffics/{email}') as resp:
                resp_json = await resp.json()
                logger.debug('Response %s', resp_json)
                return ClientTraffic(**resp_json['obj'])
        if id:
            async with self.session.get(f'panel/api/inbounds/getClientTrafficsById/{uuid}') as resp:
                resp_json = await resp.json()
                logger.debug('Response %s', resp_json)
                return ClientTraffic(**resp_json['obj'])

    @info
    async def get_tgbot_createbackup(self) -> dict[Any, Any]:
        async with self.session.get('panel/api/inbounds/createbackup') as resp:
            resp_json = await resp.json()
            logger.debug('Response %s', resp_json)
            return resp_json

    @info
    async def post_client_ips(self, email: str) -> dict[Any, Any]:
        async with self.session.post(f'panel/api/inbounds/clientIps/{email}', headers=self._headers) as resp:
            resp_json = await resp.json()
            logger.debug('Response %s', resp_json)
            return resp_json['obj']

    @info
    async def post_add_inbound(self, inbound: Inbound) -> dict[Any, Any]:
        payload = inbound.model_dump(exclude={'id', 'clientStats', 'tag'})
        async with self.session.post('panel/api/inbounds/add', headers=self._headers, data=payload) as resp:
            resp_json = await resp.json()
            logger.debug('Response %s', resp_json)
            return resp_json

    @info
    async def post_add_client_inbound(self, clients: list[Client], inboundId: int) -> dict[Any, Any]:
        clients_dump = []
        for client in clients:
            clients_dump.append(client.model_dump())
        settings = {"clients" : clients_dump }
        payload = {"id" : inboundId,
                   "settings" : json.dumps(settings) }
        async with self.session.post('panel/api/inbounds/addClient', headers=self._headers, data=payload) as resp:
            resp_json = await resp.json()
            logger.debug('Response %s', resp_json)
            return resp_json

    @info
    async def post_update_inbound(self, inbound: Inbound) -> dict[Any, Any]:
        payload = inbound.model_dump(exclude={'id', 'clientStats', 'tag'})
        async with self.session.post(f'panel/api/inbounds/update/{inbound.id}', headers=self._headers, data=payload) as resp:
            resp_json = await resp.json()
            logger.debug('Response %s', resp_json)
            return resp_json

    @info
    async def post_update_client(self, client: Client, inboundId: int , client_id: str) -> dict[Any, Any]:
        settings = {"clients" : [client.model_dump()] }
        payload = {"id" : inboundId,
                   "settings" : json.dumps(settings)}
        async with self.session.post(f'panel/api/inbounds/updateClient/{client_id}', headers=self._headers, data=payload) as resp:
            resp_json = await resp.json()
            logger.debug('Response %s', resp_json)
            return resp_json

    @info
    async def post_clear_client_ips(self, email: str) -> dict[Any, Any]:
        async with self.session.post(f'panel/api/inbounds/clearClientIps/{email}', headers=self._headers) as resp:
            resp_json = await resp.json()
            logger.debug('Response %s', resp_json)
            return resp_json

    @info
    async def post_reset_traffics_all_inbounds(self):
        async with self.session.post('panel/api/inbounds/resetAllTraffics', headers=self._headers) as resp:
            resp_json = await resp.json()
            logger.debug('Response %s', resp_json)
            return resp_json

    @info
    async def post_reset_traffics_all_clients(self, inboundId: int):
        async with self.session.post(f'panel/api/inbounds/resetAllClientTraffics/{inboundId}', headers=self._headers) as resp:
            resp_json = await resp.json()
            logger.debug('Response %s', resp_json)
            return resp_json

    @info
    async def post_reset_client_traffic(self, email: str, inboundId: int) -> dict[Any, Any]:
        async with self.session.post(f'panel/api/inbounds/{inboundId}/resetClientTraffic/{email}', headers=self._headers) as resp:
            resp_json = await resp.json()
            logger.debug('Response %s', resp_json)
            return resp_json

    @info
    async def post_delete_client(self, uuid: str, inboundId: int) -> dict[Any, Any]:
        async with self.session.post(f'panel/api/inbounds/{inboundId}/delClient/{uuid}', headers=self._headers) as resp:
            resp_json = await resp.json()
            logger.debug('Response %s', resp_json)
            return resp_json

    @info
    async def post_delete_inbound(self,inboundId: int) -> dict[Any, Any]:
        async with self.session.post(f'panel/api/inbounds/del/{inboundId}', headers=self._headers) as resp:
            resp_json = await resp.json()
            logger.debug('Response %s', resp_json)
            return resp_json

    @info
    async def post_delete_depleted_clients(self, inboundId: int) -> dict[Any, Any]:
        async with self.session.post(f'panel/api/inbounds/delDepletedClients/{inboundId}', headers=self._headers) as resp:
            resp_json = await resp.json()
            logger.debug('Response %s', resp_json)
            return resp_json

    @info
    async def post_online_clients(self) -> dict[Any, Any]:
        async with self.session.post('panel/api/inbounds/onlines', headers=self._headers) as resp:
            resp_json = await resp.json()
            logger.debug('Response %s', resp_json)
            return resp_json