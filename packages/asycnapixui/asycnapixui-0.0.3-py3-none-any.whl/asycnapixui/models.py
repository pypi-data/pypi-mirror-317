from typing import Literal

from pydantic import BaseModel


class Client(BaseModel):
    id: str
    flow: str = ""
    email: str
    limitIp: int = 0
    totalGB: int = 0
    expiryTime: int = 0
    enable: bool = False
    tgId: str = ""
    subId: str
    reset: int = 0

class ClientTraffic(BaseModel):
    id: int
    inboundId: int
    enable: bool
    email: str
    up: int
    down: int
    expiryTime: int
    total: int
    reset: int


class Inbound(BaseModel):
    id: int
    up: int = 0
    down: int = 0
    total: int = 0
    remark: str = ""
    enable: bool = False
    expiryTime: int = 0
    clientStats: list[ClientTraffic] | None = None
    #config part
    listen: str = ""
    port: int = 0
    protocol: Literal['vmess', 'vless', 'dokodemo-door', 'http', 'trojan', 'shadowsocks', 'socks', 'wireguard'] = 'vless'
    settings: str = ""
    streamSettings: str = ""
    tag: str
    sniffing: str = ""
    allocate: str = ""


