from loguru import logger
from data import config
import pyrogram
import os
from data.config import USE_PROXY,SESSIONS_PATH

async def create_sessions():
    while True:
        session_name = input('Введите название сессии (для выхода нажмите Enter)\n')
        if not session_name:
            return
        
        with open('proxy.txt','r') as file:
            proxy = [i.strip() for i in file.readlines()]
        
        if USE_PROXY:
            len_sessions = len(os.listdir(SESSIONS_PATH))
            
            if len(proxy)>len_sessions:
                
                proxy = proxy[len_sessions]
                
                proxy_client = {
                    "scheme": "socks5",
                    "hostname": proxy.split(':')[0],
                    "port": int(proxy.split(':')[1]),
                    "username": proxy.split(':')[2],
                    "password": proxy.split(':')[3],
                }
                session = pyrogram.Client(
                    api_id=config.API_ID,
                    api_hash=config.API_HASH,
                    name=session_name,
                    workdir=config.WORKDIR,
                    proxy=proxy_client
                )

                async with session:
                    user_data = await session.get_me()

                logger.success(f'Добавлена сессия +{user_data.phone_number} @{user_data.username}')
            
            else:
                session = pyrogram.Client(
                    api_id=config.API_ID,
                    api_hash=config.API_HASH,
                    name=session_name,
                    workdir=config.WORKDIR,
                )

                async with session:
                    user_data = await session.get_me()

                logger.success(f'Добавлена сессия +{user_data.phone_number} @{user_data.username}')
        else:
            session = pyrogram.Client(
                api_id=config.API_ID,
                api_hash=config.API_HASH,
                name=session_name,
                workdir=config.WORKDIR,
            )

            async with session:
                user_data = await session.get_me()

            logger.success(f'Добавлена сессия +{user_data.phone_number} @{user_data.username}')
