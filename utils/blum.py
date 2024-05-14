from pyrogram.raw.functions.messages import RequestWebView
from urllib.parse import unquote
from utils.core import logger

from fake_useragent import UserAgent
from pyrogram import Client
from data import config

import aiohttp
import asyncio
import random


class Blum:
    def __init__(self, thread: int, account: str, proxy : str):
        self.thread = thread
        if proxy:
            proxy_client = {
                "scheme": "socks5",
                "hostname": proxy.split(':')[0],
                "port": int(proxy.split(':')[1]),
                "username": proxy.split(':')[2],
                "password": proxy.split(':')[3],
            }
            self.client = Client(name=account, api_id=config.API_ID, api_hash=config.API_HASH, workdir=config.WORKDIR, proxy=proxy_client)
        else:
            self.client = Client(name=account, api_id=config.API_ID, api_hash=config.API_HASH, workdir=config.WORKDIR)
        
        if proxy:
            self.proxy = f"http://{proxy.split(':')[2]}:{proxy.split(':')[3]}@{proxy.split(':')[0]}:{proxy.split(':')[1]}"
        else:
            self.proxy = None
            
        headers = {'User-Agent': UserAgent(os='android').random}
        self.session = aiohttp.ClientSession(headers=headers, trust_env=True)

    async def main(self):
        await asyncio.sleep(random.uniform(config.ACC_DELAY[0], config.ACC_DELAY[1]))
        await self.login()

        while True:
            
            try:
                timestamp, start_time, end_time = await self.balance()
                
                await self.get_referral_info()
                await asyncio.sleep(5)
                
                await self.do_tasks()
                await asyncio.sleep(5)
                
                if start_time is None and end_time is None:
                    await self.start()
                    logger.info(f"Thread {self.thread} | Start farming!")

                elif start_time is not None and end_time is not None and timestamp >= end_time:
                    timestamp, balance = await self.claim()
                    logger.success(f"Thread {self.thread} | Claimed reward! Balance: {balance}")

                else:
                    logger.info(f"Thread {self.thread} | Sleep {end_time-timestamp} seconds!")
                    await asyncio.sleep(end_time-timestamp)

                await asyncio.sleep(60)
            except Exception as e:
                logger.error(f"Thread {self.thread} | Error: {e}")
                await asyncio.sleep(60)

    async def claim(self):
        resp = await self.session.post("https://game-domain.blum.codes/api/v1/farming/claim",proxy = self.proxy)
        resp_json = await resp.json()

        return int(resp_json.get("timestamp")/1000), resp_json.get("availableBalance")

    async def start(self):
        resp = await self.session.post("https://game-domain.blum.codes/api/v1/farming/start",proxy = self.proxy)

    async def balance(self):
        resp = await self.session.get("https://game-domain.blum.codes/api/v1/user/balance",proxy = self.proxy)
        resp_json = await resp.json()
        timestamp = resp_json.get("timestamp")
        if resp_json.get("farming"):
            start_time = resp_json.get("farming").get("startTime")
            end_time = resp_json.get("farming").get("endTime")
            return int(timestamp/1000), int(start_time/1000), int(end_time/1000)
        return int(timestamp/1000), None, None

    async def login(self):
        json_data = {"query": await self.get_tg_web_data()}

        resp = await self.session.post("https://gateway.blum.codes/v1/auth/provider/PROVIDER_TELEGRAM_MINI_APP", json=json_data,proxy = self.proxy)
        self.session.headers['Authorization'] = "Bearer " + (await resp.json()).get("token").get("access")

    async def get_tg_web_data(self):
        await self.client.connect()
        
        web_view = await self.client.invoke(RequestWebView(
            peer=await self.client.resolve_peer('BlumCryptoBot'),
            bot=await self.client.resolve_peer('BlumCryptoBot'),
            platform='android',
            from_bot_menu=False,
            url='https://telegram.blum.codes/'
        ))

        auth_url = web_view.url
        await self.client.disconnect()
        return unquote(string=unquote(string=auth_url.split('tgWebAppData=')[1].split('&tgWebAppVersion')[0]))
    
    async def get_referral_info(self):
        resp = await self.session.get("https://gateway.blum.codes/v1/friends/balance",proxy = self.proxy)
        resp_json = await resp.json()
        if resp_json['canClaim'] == True:
            claimed = await self.claim_referral()
            logger.success(f"Thread {self.thread} | Claimed referral reward! Claimed: {claimed}")
        
    
    async def claim_referral(self):
        resp = await self.session.post("https://game-domain.blum.codes/api/v1/farming/claim",proxy = self.proxy)
        resp_json = await resp.json()
        return resp_json['claimBalance']
    
    async def do_tasks(self):
        resp = await self.session.get("https://game-domain.blum.codes/api/v1/tasks",proxy = self.proxy)
        resp_json = await resp.json()
        for task in resp_json:
            if task['status'] == "NOT_STARTED":
                await self.session.post(f"https://game-domain.blum.codes/api/v1/tasks/{task['id']}/start",proxy=self.proxy)
                await asyncio.sleep(3)
            elif task['status'] == "DONE":
                answer = await self.session.post(f"https://game-domain.blum.codes/api/v1/tasks/{task['id']}/claim",proxy=self.proxy)
                answer = await answer.json()
                logger.success(f"Thread {self.thread} | Claimed TASK reward! Claimed: {answer['reward']}")
                await asyncio.sleep(3)
