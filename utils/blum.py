from pyrogram.raw.functions.messages import RequestWebView
from urllib.parse import unquote
from utils.core import logger
from datetime import datetime
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
        self.auth_token = ""
        self.ref_token=""
        headers = {'User-Agent': UserAgent(os='android').random}
        self.session = aiohttp.ClientSession(headers=headers, trust_env=True)

    async def main(self):
        await asyncio.sleep(random.uniform(config.ACC_DELAY[0], config.ACC_DELAY[1]))
        await self.login()
        
        logger.info(f"Thread {self.thread} | Start!")
        while True:
            try:
                valid = await self.is_token_valid()
                if not valid:
                    logger.warning(f"Thread {self.thread} | Token is invalid. Refreshing token...")
                    await self.refresh_token()
                await asyncio.sleep(5)
                
                await self.claim_diamond()
                await asyncio.sleep(5)
                
                timestamp, start_time, end_time = await self.balance()
                await self.get_referral_info()
                await asyncio.sleep(5)
                
                await self.do_tasks()
                await asyncio.sleep(5)
                
                if config.SPEND_DIAMONDS:
                    diamonds_balance = await self.get_diamonds_balance()
                    for count in range(diamonds_balance):
                        logger.info(f"Thread {self.thread} | Have {diamonds_balance-count} diamonds!")
                        await self.game()
                        await asyncio.sleep(random.randint(*config.SLEEP_GAME_TIME))
                        
                if start_time is None and end_time is None:
                    await self.start()
                    logger.info(f"Thread {self.thread} | Start farming!")
                elif start_time is not None and end_time is not None and timestamp >= end_time:
                    timestamp, balance = await self.claim()
                    logger.success(f"Thread {self.thread} | Claimed reward! Balance: {balance}")
                
                else:
                    logger.info(f"Thread {self.thread} | Sleep {(end_time-timestamp)} seconds!")
                    await asyncio.sleep(end_time-timestamp)
                await asyncio.sleep(60)
            except Exception as err:
                logger.error(f"main | Thread {self.thread} | {err}")


    async def claim(self):
        try:
            resp = await self.session.post("https://game-domain.blum.codes/api/v1/farming/claim",proxy = self.proxy)
            resp_json = await self.parse_json_response(resp)
            return int(resp_json.get("timestamp")/1000), resp_json.get("availableBalance")
        except:
            pass

    async def start(self):
        try:
            resp = await self.session.post("https://game-domain.blum.codes/api/v1/farming/start",proxy = self.proxy)
        except:
            pass
        
    async def balance(self):
        try:
            
            resp = await self.session.get("https://game-domain.blum.codes/api/v1/user/balance",proxy = self.proxy)
            resp_json = await self.parse_json_response(resp)
            timestamp = resp_json.get("timestamp")
            if resp_json.get("farming"):
                start_time = resp_json.get("farming").get("startTime")
                end_time = resp_json.get("farming").get("endTime")
                return int(timestamp/1000), int(start_time/1000), int(end_time/1000)
            return int(timestamp), None, None
        except:
            pass

    async def login(self):
        
        json_data = {"query": await self.get_tg_web_data()}
        resp = await self.session.post("https://gateway.blum.codes/v1/auth/provider/PROVIDER_TELEGRAM_MINI_APP", json=json_data,proxy = self.proxy)
        resp = await self.parse_json_response(resp)
        self.ref_token = resp.get("token").get("refresh")
        self.session.headers['Authorization'] = "Bearer " + (resp).get("token").get("access")

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
        resp_json = await self.parse_json_response(resp)
        if resp_json['canClaim'] == True:
            claimed = await self.claim_referral()
            logger.success(f"get_ref | Thread {self.thread} | Claimed referral reward! Claimed: {claimed}")
        
    
    async def claim_referral(self):
        resp = await self.session.post("https://gateway.blum.codes/v1/friends/claim",proxy = self.proxy)
        resp_json = await self.parse_json_response(resp)
        return resp_json['claimBalance']
    
    async def do_tasks(self):
        resp = await self.session.get("https://game-domain.blum.codes/api/v1/tasks",proxy = self.proxy)
        resp_json = await self.parse_json_response(resp)
        try:
            for task in resp_json:
                if task['status'] == "NOT_STARTED":
                    await self.session.post(f"https://game-domain.blum.codes/api/v1/tasks/{task['id']}/start",proxy=self.proxy)
                    await asyncio.sleep(3)
                elif task['status'] == "DONE":
                    answer = await self.session.post(f"https://game-domain.blum.codes/api/v1/tasks/{task['id']}/claim",proxy=self.proxy)
                    answer = await answer.json()
                    logger.success(f"Thread {self.thread} | Claimed TASK reward! Claimed: {answer['reward']}")
                    await asyncio.sleep(3)
        except Exception as err:
            logger.error(f"do_task | Thread {self.thread} | {err}")
    
    async def is_token_valid(self):
        response = await self.session.get("https://gateway.blum.codes/v1/user/me",proxy=self.proxy)
        
        if response.status == 200:
            return True
        elif response.status == 401:
            error_info = await response.json()
            return error_info.get("code") != 16
        else:
            return False
    
    async def refresh_token(self):

        
        refresh_payload = {
            'refresh': self.ref_token  # The refresh token in the request body
        }
        
        if "authorization" in self.session.headers:
            del self.session.headers['authorization']
            
        response = await self.session.post("https://gateway.blum.codes/v1/auth/refresh",json=refresh_payload,proxy=self.proxy)
        
        if response.status == 200:
            data = await response.json()  
            new_access_token = data.get("access")  
            new_refresh_token = data.get("refresh")

            if new_access_token:
                self.auth_token = new_access_token  
                self.ref_token = new_refresh_token  
                self.session.headers['Authorization'] = "Bearer "+self.auth_token
                logger.info(f"refresh | Thread {self.thread} | Token refreshed successfully.")
            else:
                raise Exception("New access token not found in the response")
        else:
            raise Exception("Failed to refresh the token")
    
    async def get_diamonds_balance(self):
        resp = await self.session.get("https://game-domain.blum.codes/api/v1/user/balance",proxy = self.proxy)
        resp_json = await resp.json()
        return resp_json['playPasses']
    
    async def game(self):

        response = await self.session.post('https://game-domain.blum.codes/api/v1/game/play', proxy=self.proxy)
        logger.info(f"Thread {self.thread} | Start DROP GAME!")
        if 'message' in await response.json():
            logger.error(f"game | Thread {self.thread} | DROP GAME CAN'T START")
            return
        text = (await response.json())['gameId']
        await asyncio.sleep(30)
        count = random.randint(*config.POINTS)
        
        json_data = {
            'gameId': text,
            'points': count,
        }

        response = await self.session.post('https://game-domain.blum.codes/api/v1/game/claim', json=json_data, proxy=self.proxy)
        
        if await response.text() == "OK":
            logger.success(f"Thread {self.thread} | Claimed DROP GAME ! Claimed: {count}")
        else:
            logger.error(f"Thread {self.thread} | {await response.text()}")
    
    async def claim_diamond(self):

        resp = await self.session.post("https://game-domain.blum.codes/api/v1/daily-reward?offset=-180", proxy=self.proxy)
        txt = await resp.text()
        
        return True if txt == 'OK' else txt

    async def parse_json_response(self, response):
        if response.headers.get('Content-Type') == 'application/json':
            return await response.json()
        else:
            logger.error(f"Unexpected content type: {response.headers.get('Content-Type')}. Response: {await response.text()}")
            response.raise_for_status()
