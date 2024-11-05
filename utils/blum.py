from pyrogram.raw.functions.messages import RequestWebView
from urllib.parse import unquote
from utils.core import logger
from fake_useragent import UserAgent
from pyrogram import Client
from data import config
from utils.payload import get_payload
import aiohttp
import asyncio
import random
import re
import json
import os

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
        
        ua = self.set_useragent()
        headers = {
            'accept': 'application/json, text/plain, */*',
            'cache-control': 'no-cache',
            'content-type': 'application/json',
            'origin': 'https://telegram.blum.codes',
            'pragma': 'no-cache',
            'priority': 'u=1, i',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': ua}
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
                
                if config.DO_TASKS:
                    await self.do_tasks()
                    await asyncio.sleep(random.randint(*config.MINI_SLEEP))
                
                if config.DROP_GAME:
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
            if 'message' in resp_json:
                if not (await self.is_token_valid()):
                    await self.refresh()
                return 0
            return int(resp_json.get("timestamp")/1000), resp_json.get("availableBalance")
        except:
            pass

    async def start(self):
        try:
            resp = await self.session.post("https://game-domain.blum.codes/api/v1/farming/start",proxy = self.proxy)
            resp_json = await resp.json()
            if 'message' in resp_json:
                if not (await self.is_token_valid()):
                    await self.refresh()
                return 0
        except:
            pass
        
    async def balance(self):
        try:
            
            resp = await self.session.get("https://game-domain.blum.codes/api/v1/user/balance",proxy = self.proxy)
            resp_json = await resp.json()
            if 'message' in resp_json:
                if not (await self.is_token_valid()):
                    await self.refresh()
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
            resp = await self.session.post("https://user-domain.blum.codes/api/v1/auth/provider/PROVIDER_TELEGRAM_MINI_APP", json=json_data,proxy = self.proxy)
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
            resp = await self.session.get("https://user-domain.blum.codes/api/v1/friends/balance",proxy = self.proxy)
            resp_json = await resp.json()
            if 'message' in resp_json:
                if not (await self.is_token_valid()):
                    await self.refresh()
                return 0
            if resp_json['canClaim'] == True:
                claimed = await self.claim_referral()
                logger.success(f"get_ref | Thread {self.thread} | {self.name} | Claimed referral reward! Claimed: {claimed}")
        except:
            pass
    
    async def claim_referral(self):
        resp = await self.session.post("https://user-domain.blum.codes/api/v1/friends/claim",proxy = self.proxy)
        resp_json = await resp.json()
        if 'message' in resp_json:
            if not (await self.is_token_valid()):
                await self.refresh()
            return 0
        return resp_json['claimBalance']
    
    async def do_tasks(self):
        resp = await self.session.get("https://earn-domain.blum.codes/api/v1/tasks",proxy = self.proxy)
        resp_json = (await resp.json())
        if 'message' in resp_json:
            if not (await self.is_token_valid()):
                await self.refresh()
            return 0
        try:
            for tasks_all in resp_json:
                if tasks_all['sectionType']=="DEFAULT":
                    for task in tasks_all['subSections']:
                        if task['title'] == "Frens":
                            continue
                        tasks = task['tasks']
                        for task in tasks:
                            if 'isHidden' in task:
                                if not task['isHidden']:
                                    if task['status'] == "NOT_STARTED":
                                        await self.session.post(f"https://earn-domain.blum.codes/api/v1/tasks/{task['id']}/start",proxy=self.proxy)
                                        await asyncio.sleep(random.randint(*config.MINI_SLEEP))
                                    elif task['status'] == "READY_FOR_CLAIM":
                                        answer = await self.session.post(f"https://earn-domain.blum.codes/api/v1/tasks/{task['id']}/claim",proxy=self.proxy)
                                        answer = await answer.json()
                                        if 'message' in answer:
                                            continue
                                        logger.success(f"tasks | Thread {self.thread} | {self.name} | Claimed TASK reward! Claimed: {answer['reward']}")
                                        await asyncio.sleep(random.randint(*config.MINI_SLEEP))
                            else:
                                if task['status'] == "NOT_STARTED":
                                    await self.session.post(f"https://earn-domain.blum.codes/api/v1/tasks/{task['id']}/start",proxy=self.proxy)
                                    await asyncio.sleep(random.randint(*config.MINI_SLEEP))
                                elif task['status'] == "READY_FOR_CLAIM":
                                    answer = await self.session.post(f"https://earn-domain.blum.codes/api/v1/tasks/{task['id']}/claim",proxy=self.proxy)
                                    answer = await answer.json()
                                    if 'message' in answer:
                                        continue
                                    logger.success(f"tasks | Thread {self.thread} | {self.name} | Claimed TASK reward! Claimed: {answer['reward']}")
                                    await asyncio.sleep(random.randint(*config.MINI_SLEEP))
        except Exception as err:
            logger.error(f"tasks | Thread {self.thread} | {self.name} | {err}")
    
    async def is_token_valid(self):
        response = await self.session.get("https://user-domain.blum.codes/api/v1/user/me",proxy=self.proxy)
        
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
            
        response = await self.session.post("https://user-domain.blum.codes/api/v1/auth/refresh",json=refresh_payload,proxy=self.proxy)
        
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
        if 'message' in resp_json:
            if not (await self.is_token_valid()):
                await self.refresh()
            return 0
        return resp_json['playPasses']
    
    

    async def claim_game(self, game_id: str, freeze_count):
        try:
            points = str(random.randint(*config.POINTS))
            trump = str(random.randint(*[4,8]))
            harris = str(random.randint(*[4,8]))

            data = await get_payload(game_id, points, trump, harris, freeze_count)
            

            resp = await self.session.post(f"https://game-domain.blum.codes/api/v2/game/claim", json={'payload': data},
                                          proxy=self.proxy)
            if resp.status != 200:
                resp = await self.session.post(f"https://game-domain.blum.codes/api/v2/game/claim", json={'payload': data},
                                              proxy=self.proxy)

            txt = await resp.text()
            if txt == 'OK':
                logger.success(f"game | Thread {self.thread} | {self.name} | Claimed DROP GAME ! Claimed: {points}")
            return True if txt == 'OK' else txt, points
        except Exception as e:
            logger.error(f"Error occurred during claim game: {e}")

    async def start_game(self):
        try:
            resp = await self.session.post(f"https://game-domain.blum.codes/api/v2/game/play", proxy=self.proxy)
            response_data = await resp.json()
            if "gameId" in response_data:
                logger.info(f"game | Thread {self.thread} | {self.name} | Start DROP GAME!")
                return response_data.get("gameId")
            elif "message" in response_data:
                logger.error(f"game | Thread {self.thread} | {self.name} | DROP GAME CAN'T START")
                return response_data.get("message")
        except Exception as e:
            logger.error(f"Error occurred during start game: {e}")

    async def game(self):
        try:
            game_id = await self.start_game()
            
            if not game_id or game_id == "cannot start game":
                return False
            
            count = random.randint(*config.POINTS)
            freeze_count = random.randint(*[4,8])
            await asyncio.sleep(30 + freeze_count * 5)

            msg, points = await self.claim_game(game_id, freeze_count)
            print(msg,points)
        except Exception as err:
            logger.error(f"game | Thread {self.thread} | {self.name} | {err}")
    
    async def claim_diamond(self):
        resp = await self.session.post("https://game-domain.blum.codes/api/v1/daily-reward?offset=-180", proxy=self.proxy)
        txt = await resp.text()
        if 'message' in txt:
            if not (await self.is_token_valid()):
                await self.refresh()
                return False
        return True if txt == 'OK' else txt
    
    def set_useragent(self):
        try:
            file_path = f"data/useragents.json"

            if not os.path.exists(file_path):
                data = {self.name: self.generate_user_agent()}
                with open(file_path, 'w', encoding="utf-8") as file:
                    json.dump(data, file, ensure_ascii=False, indent=4)

                return data[self.name]
            else:
                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        content = file.read()
                        data = json.loads(content)

                    if self.name in data:
                        return data[self.name]

                    else:
                        data[self.name] = self.generate_user_agent()

                        with open(file_path, 'w', encoding='utf-8') as file:
                            file.write(json.dumps(data, ensure_ascii=False, indent=4))

                        return data[self.name]
                except json.decoder.JSONDecodeError:
                    logger.error(f"useragent | Thread {self.thread} | {self.name} | syntax error in UserAgents json file!")
                    return 'Mozilla/5.0 (Linux; Android 5.1.1; SAMSUNG SM-G920FQ Build/LRX22G) AppleWebKit/533.2 (KHTML, like Gecko) Chrome/50.0.1819.308 Mobile Safari/601.9'

        except Exception as err:
            logger.error(f"useragent | Thread {self.thread} | {self.name} | {err}")
            return 'Mozilla/5.0 (Linux; Android 5.1.1; SAMSUNG SM-G920FQ Build/LRX22G) AppleWebKit/533.2 (KHTML, like Gecko) Chrome/50.0.1819.308 Mobile Safari/601.9'
    

    def extract_chrome_version(self, user_agent):
        match = re.search(r'Chrome/(\d+\.\d+\.\d+\.\d+)', user_agent)
        if match:
            return match.group(1).split('.')[0]
        return 122
    
    def generate_user_agent(self):
        chrome_versions = [
            "110.0.5481.100", "110.0.5481.104", "110.0.5481.105", 
            "110.0.5481.106", "110.0.5481.107", "110.0.5481.110", 
            "110.0.5481.111", "110.0.5481.115", "110.0.5481.118", 
            "110.0.5481.120", "111.0.5563.62", "111.0.5563.64", 
            "111.0.5563.66", "111.0.5563.67", "111.0.5563.68", 
            "112.0.5615.49", "112.0.5615.51", "112.0.5615.53", 
            "112.0.5615.54", "112.0.5615.55", "113.0.5672.63", 
            "113.0.5672.64", "113.0.5672.66", "113.0.5672.67", 
            "113.0.5672.68", "114.0.5735.90", "114.0.5735.91", 
            "114.0.5735.92", "114.0.5735.93", "114.0.5735.94", 
            "115.0.5790.102", "115.0.5790.103", "115.0.5790.104", 
            "115.0.5790.105", "115.0.5790.106", "116.0.5845.97", 
            "116.0.5845.98", "116.0.5845.99", "116.0.5845.100", 
            "116.0.5845.101", "117.0.5938.62", "117.0.5938.63", 
            "117.0.5938.64", "117.0.5938.65", "117.0.5938.66", 
            "118.0.5993.90", "118.0.5993.91", "118.0.5993.92", 
            "118.0.5993.93", "118.0.5993.94", "119.0.6049.43", 
            "119.0.6049.44", "119.0.6049.45", "119.0.6049.46", 
            "119.0.6049.47", "120.0.6138.72", "120.0.6138.73", 
            "120.0.6138.74", "120.0.6138.75", "120.0.6138.76", 
            "121.0.6219.29", "121.0.6219.30", "121.0.6219.31", 
            "121.0.6219.32", "121.0.6219.33", "122.0.6308.16", 
            "122.0.6308.17", "122.0.6308.18", "122.0.6308.19", 
            "122.0.6308.20", "123.0.6374.92", "123.0.6374.93", 
            "123.0.6374.94", "123.0.6374.95", "123.0.6374.96", 
            "124.0.6425.5", "124.0.6425.6", "124.0.6425.7", 
            "124.0.6425.8", "124.0.6425.9", "125.0.6544.32", 
            "125.0.6544.33", "125.0.6544.34", "125.0.6544.35", 
            "125.0.6544.36", "126.0.6664.99", "126.0.6664.100", 
            "126.0.6664.101", "126.0.6664.102", "126.0.6664.103", 
            "127.0.6780.73", "127.0.6780.74", "127.0.6780.75", 
            "127.0.6780.76", "127.0.6780.77", "128.0.6913.45", 
            "128.0.6913.46", "128.0.6913.47", "128.0.6913.48", 
            "128.0.6913.49", "129.0.7026.88", "129.0.7026.89", 
            "129.0.7026.90", "129.0.7026.91", "129.0.7026.92"
        ]

        
        android_devices = [
            "SAMSUNG SM-N975F", "SAMSUNG SM-G973F", "SAMSUNG SM-G991B", 
            "SAMSUNG SM-G996B", "SAMSUNG SM-A325F", "SAMSUNG SM-A525F", 
            "Xiaomi Redmi Note 11", "POCO X3 Pro", "POCO F3", 
            "Xiaomi Mi 11", "Samsung Galaxy S21", "Samsung Galaxy S22", 
            "Samsung Galaxy S23", "Samsung Galaxy A52", "Samsung Galaxy A53", 
            "Samsung Galaxy M32", "Xiaomi 12", "OnePlus 9", 
            "OnePlus Nord 2", "Realme GT", "Nokia G50",
            "Huawei P40 Lite", "Honor 50"
        ]

        
        windows_versions = [
            "10.0", "11.0", "12.0"
        ]
        
        platforms = [
            f"Mozilla/5.0 (Windows NT {random.choice(windows_versions)}; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.choice(chrome_versions)} Safari/537.36",
            f"Mozilla/5.0 (Linux; Android {random.randint(11, 13)}; {random.choice(android_devices)}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.choice(chrome_versions)} Mobile Safari/537.36"
        ]
        
        return random.choice(platforms)

