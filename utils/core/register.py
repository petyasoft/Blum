from loguru import logger
from data import config
import pyrogram
from data.config import USE_PROXY
import random

async def create_sessions():
    while True:
        session_name = input('Введите название сессии (для выхода нажмите Enter)\n')
        if not session_name:
            return
        
        with open('fake_info.txt','r') as file:
            fake_info = [i.strip() for i in file.readlines()]
                
        if USE_PROXY:
            proxy_dict = {}
            with open('proxy.txt','r') as file:
                proxy_list = [i.strip().split() for i in file.readlines() if len(i.strip().split()) == 2]
                for prox,name in proxy_list:
                    proxy_dict[name] = prox
            
            if session_name in proxy_dict:
                proxy = proxy_dict[session_name]
                proxy_client = {
                    "scheme": config.PROXY_TYPE,
                    "hostname": proxy.split(':')[0],
                    "port": int(proxy.split(':')[1]),
                    "username": proxy.split(':')[2],
                    "password": proxy.split(':')[3],
                }
                add_info = random.choice(fake_info)
                
                session = pyrogram.Client(
                    api_id=config.API_ID,
                    api_hash=config.API_HASH,
                    name=session_name,
                    workdir=config.WORKDIR,
                    proxy=proxy_client,
                    device_model=add_info[0],
                    system_version=add_info[1],
                    app_version=add_info[2],
                    lang_code=add_info[3]
                )

                async with session:
                    user_data = await session.get_me()

                logger.success(f'Добавлена сессия +{user_data.phone_number} @{user_data.username} PROXY {proxy.split(":")[0]}')
            else:
                add_info = random.choice(fake_info)
                
                session = pyrogram.Client(
                    api_id=config.API_ID,
                    api_hash=config.API_HASH,
                    name=session_name,
                    workdir=config.WORKDIR,
                    device_model=add_info[0],
                    system_version=add_info[1],
                    app_version=add_info[2],
                    lang_code=add_info[3]
                )

                async with session:
                    user_data = await session.get_me()

                logger.success(f'Добавлена сессия +{user_data.phone_number} @{user_data.username} PROXY : NONE')
        else:
            add_info = random.choice(fake_info)
            
            session = pyrogram.Client(
                api_id=config.API_ID,
                api_hash=config.API_HASH,
                name=session_name,
                workdir=config.WORKDIR,
                device_model=add_info[0],
                system_version=add_info[1],
                app_version=add_info[2],
                lang_code=add_info[3]
            )

            async with session:
                user_data = await session.get_me()

            logger.success(f'Добавлена сессия +{user_data.phone_number} @{user_data.username} PROXY : NONE')
