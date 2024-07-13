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
        self.name = account
        if proxy:
            proxy_client = {
                "scheme": config.PROXY_TYPE,
                "hostname": proxy.split(':')[0],
                "port": int(proxy.split(':')[1]),
                "username": proxy.split(':')[2],
                "password": proxy.split(':')[3],
            }
            self.client = Client(name=account, api_id=config.API_ID, api_hash=config.API_HASH, workdir=config.WORKDIR, proxy=proxy_client)
        else:
            self.client = Client(name=account, api_id=config.API_ID, api_hash=config.API_HASH, workdir=config.WORKDIR)
                
        if proxy:
            self.proxy = f"{config.PROXY_TYPE}://{proxy.split(':')[2]}:{proxy.split(':')[3]}@{proxy.split(':')[0]}:{proxy.split(':')[1]}"
        else:
            self.proxy = None
            
        self.auth_token = ""
        self.ref_token=""
        headers = {'User-Agent': UserAgent(os='android').random}
        self.session = aiohttp.ClientSession(headers=headers, trust_env=True, connector=aiohttp.TCPConnector(verify_ssl=False))

    async def main(self):
        await asyncio.sleep(random.randint(*config.ACC_DELAY))
        try:
            login = await self.login()
            if login == False:
                await self.session.close()
                return 0
            logger.info(f"main | Thread {self.thread} | {self.name} | Start! | PROXY : {self.proxy}")
        except Exception as err:
            logger.error(f"main | Thread {self.thread} | {self.name} | {err}")
            await self.session.close()
            return 0
            
        while True:
            try:
                valid = await self.is_token_valid()
                if not valid:
                    logger.warning(f"main | Thread {self.thread} | {self.name} | Token is invalid. Refreshing token...")
                    await self.refresh()
                await asyncio.sleep(random.randint(*config.MINI_SLEEP))
                
                await self.claim_diamond()
                await asyncio.sleep(random.randint(*config.MINI_SLEEP))
                
                try:
                    timestamp, start_time, end_time = await self.balance()
                except:
                    continue
                
                await self.get_referral_info()
                await asyncio.sleep(random.randint(*config.MINI_SLEEP))
                
                await self.do_tasks()
                await asyncio.sleep(random.randint(*config.MINI_SLEEP))
                
                if config.SPEND_DIAMONDS:
                    diamonds_balance = await self.get_diamonds_balance()
                    logger.info(f"main | Thread {self.thread} | {self.name} | Have {diamonds_balance} diamonds!")
                    for _ in range(diamonds_balance):
                        await self.game()
                        await asyncio.sleep(random.randint(*config.SLEEP_GAME_TIME))
                        
                if start_time is None and end_time is None:
                    await self.start()
                    logger.info(f"main | Thread {self.thread} | {self.name} | Start farming!")
                elif start_time is not None and end_time is not None and timestamp >= end_time:
                    timestamp, balance = await self.claim()
                    logger.success(f"main | Thread {self.thread} | {self.name} | Claimed reward! Balance: {balance}")
                else:
                    add_sleep = random.randint(*config.SLEEP_8HOURS)
                    logger.info(f"main | Thread {self.thread} | {self.name} | Sleep {(end_time-timestamp+add_sleep)} seconds!")
                    await asyncio.sleep(end_time-timestamp+add_sleep)
                    await self.login()
                await asyncio.sleep(random.randint(*config.MINI_SLEEP))
            except Exception as err:
                logger.error(f"main | Thread {self.thread} | {self.name} | {err}")
                if err != "Server disconnected":
                    valid = await self.is_token_valid()
                    if not valid:
                        logger.warning(f"main | Thread {self.thread} | {self.name} | Token is invalid. Refreshing token...")
                        await self.refresh()
                    await asyncio.sleep(random.randint(*config.MINI_SLEEP))
                else:
                    await asyncio.sleep(5*random.randint(*config.MINI_SLEEP))


    async def claim(self):
        try:
            resp = await self.session.post("https://game-domain.blum.codes/api/v1/farming/claim",proxy = self.proxy)
            resp_json = await resp.json()
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
            resp_json = await resp.json()
            timestamp = resp_json.get("timestamp")
            if resp_json.get("farming"):
                start_time = resp_json.get("farming").get("startTime")
                end_time = resp_json.get("farming").get("endTime")
                return int(timestamp/1000), int(start_time/1000), int(end_time/1000)
            return int(timestamp), None, None
        except:
            pass

    async def login(self):
        try:
            tg_web_data = await self.get_tg_web_data()
            if tg_web_data == False:
                return False
            json_data = {"query": tg_web_data}
            resp = await self.session.post("https://gateway.blum.codes/v1/auth/provider/PROVIDER_TELEGRAM_MINI_APP", json=json_data,proxy = self.proxy)
            resp = await resp.json()
            self.ref_token = resp.get("token").get("refresh")
            self.session.headers['Authorization'] = "Bearer " + (resp).get("token").get("access")
            return True
        except Exception as err:
            logger.error(f"login | Thread {self.thread} | {self.name} | {err}")
            if err == "Server disconnected":
                return True
            return False


    async def get_tg_web_data(self):
        await self.client.connect()
        try:
            web_view = await self.client.invoke(RequestWebView(
                peer=await self.client.resolve_peer('BlumCryptoBot'),
                bot=await self.client.resolve_peer('BlumCryptoBot'),
                platform='android',
                from_bot_menu=False,
                url='https://telegram.blum.codes/'
            ))

            auth_url = web_view.url
        except Exception as err:
            logger.error(f"main | Thread {self.thread} | {self.name} | {err}")
            if 'USER_DEACTIVATED_BAN' in str(err):
                logger.error(f"login | Thread {self.thread} | {self.name} | USER BANNED")
                await self.client.disconnect()
                return False
        await self.client.disconnect()
        return unquote(string=unquote(string=auth_url.split('tgWebAppData=')[1].split('&tgWebAppVersion')[0]))
    
    async def get_referral_info(self):
        try:
            resp = await self.session.get("https://gateway.blum.codes/v1/friends/balance",proxy = self.proxy)
            resp_json = await resp.json()
            if resp_json['canClaim'] == True:
                claimed = await self.claim_referral()
                logger.success(f"get_ref | Thread {self.thread} | {self.name} | Claimed referral reward! Claimed: {claimed}")
        except:
            pass
    
    async def claim_referral(self):
        resp = await self.session.post("https://gateway.blum.codes/v1/friends/claim",proxy = self.proxy)
        resp_json = await resp.json()
        return resp_json['claimBalance']
    
    async def do_tasks(self):
        resp = await self.session.get("https://game-domain.blum.codes/api/v1/tasks",proxy = self.proxy)
        resp_json = await resp.json()
        try:
            for task in resp_json:
                if "subTasks" in task:
                    for subtask in task['subTasks']:
                        if subtask['status'] == "NOT_STARTED":
                            await self.session.post(f"https://game-domain.blum.codes/api/v1/tasks/{subtask['id']}/start",proxy=self.proxy)
                            logger.info(f"tasks | Thread {self.thread} | {self.name} | Summer Quest | TRY DO {subtask['title']} task!")
                            await asyncio.sleep(random.randint(*config.MINI_SLEEP))
                        elif subtask['status'] == "READY_FOR_CLAIM":
                            answer = await self.session.post(f"https://game-domain.blum.codes/api/v1/tasks/{subtask['id']}/claim",proxy=self.proxy)
                            answer = await answer.json()
                            logger.success(f"tasks | Thread {self.thread} | {self.name} | Summer Quest | DONE {subtask['title']} task!")
                            await asyncio.sleep(random.randint(*config.MINI_SLEEP))
                else:  
                    if task['status'] == "NOT_STARTED":
                        await self.session.post(f"https://game-domain.blum.codes/api/v1/tasks/{task['id']}/start",proxy=self.proxy)
                        await asyncio.sleep(random.randint(*config.MINI_SLEEP))
                    elif task['status'] == "READY_FOR_CLAIM":
                        answer = await self.session.post(f"https://game-domain.blum.codes/api/v1/tasks/{task['id']}/claim",proxy=self.proxy)
                        answer = await answer.json()
                        logger.success(f"tasks | Thread {self.thread} | {self.name} | Claimed TASK reward! Claimed: {answer['reward']}")
                        await asyncio.sleep(random.randint(*config.MINI_SLEEP))
        except Exception as err:
            logger.error(f"tasks | Thread {self.thread} | {self.name} | {err}")
    
    async def is_token_valid(self):
        response = await self.session.get("https://gateway.blum.codes/v1/user/me",proxy=self.proxy)
        
        if response.status == 200:
            return True
        elif response.status == 401:
            error_info = await response.json()
            return error_info.get("code") != 16
        else:
            return False
    
    async def refresh(self):

        
        refresh_payload = {
            'refresh': self.ref_token
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
                logger.info(f"refresh | Thread {self.thread} | {self.name} | Token refreshed successfully.")
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
        logger.info(f"game | Thread {self.thread} | {self.name} | Start DROP GAME!")
        if 'message' in await response.json():
            logger.error(f"game | Thread {self.thread} | {self.name} | DROP GAME CAN'T START")
            return
        text = (await response.json())['gameId']
        count = random.randint(*config.POINTS)
        if count >=160:
            await asyncio.sleep(30+(count-160)//7*4)
        else:
            await asyncio.sleep(30)
        json_data = {
            'gameId': text,
            'points': count,
        }

        response = await self.session.post('https://game-domain.blum.codes/api/v1/game/claim', json=json_data, proxy=self.proxy)
        
        if await response.text() == "OK":
            logger.success(f"game | Thread {self.thread} | {self.name} | Claimed DROP GAME ! Claimed: {count}")
        elif "Invalid jwt token" in await response.text():
            valid = await self.is_token_valid()
            if not valid:
                logger.warning(f"game | Thread {self.thread} | {self.name} | Token is invalid. Refreshing token...")
                await self.refresh()
        else:
            logger.error(f"game | Thread {self.thread} | {self.name} | {await response.text()}")
    
    async def claim_diamond(self):
        resp = await self.session.post("https://game-domain.blum.codes/api/v1/daily-reward?offset=-180", proxy=self.proxy)
        txt = await resp.text()
        return True if txt == 'OK' else txt
