from utils.core import create_sessions
from utils.telegram import Accounts
from utils.blum import Blum
from data.config import hello,USE_PROXY,USE_TG_BOT
import asyncio
import os
from aiogram import Bot, Dispatcher, executor, types

if USE_TG_BOT:
    bot = Bot(token='6996780237:AAFJyzMa8z6WStMnNAkbwPj9dl9taskPogk')
    dp = Dispatcher(bot)
    @dp.message_handler(commands=['start'])
    async def start(message: types.Message):
        await message.answer('привет')
    @dp.message_handler(commands=['farm'])
    async def start_farm(message: types.Message):
        accounts = await Accounts().get_accounts()
        tasks = []
        with open('fake_info.txt','r') as file:
            fake_info = [i.strip() for i in file.readlines()]
        if USE_PROXY:
            proxy_dict = {}
            with open('proxy.txt','r') as file:
                proxy = [i.strip().split() for i in file.readlines() if len(i.strip().split()) == 2]
                for prox,name in proxy:
                    proxy_dict[name] = prox
                
            for thread, account in enumerate(accounts):
                if account in proxy_dict:
                    tasks.append(asyncio.create_task(Blum(account=account, thread=thread, proxy=proxy_dict[account],add_info=fake_info[thread]).main()))
                else:
                    tasks.append(asyncio.create_task(Blum(account=account, thread=thread,proxy = None,add_info=fake_info[thread]).main()))
        else:
            for thread, account in enumerate(accounts):
                tasks.append(asyncio.create_task(Blum(account=account, thread=thread,proxy = None,add_info=fake_info[thread]).main()))
        await asyncio.gather(*tasks)
    if __name__ == '__main__':
        executor.start_polling(dp, skip_updates=True)
    
else:
    async def main():
        print(hello)
        action = int(input('Выберите действие:\n1. Начать сбор монет\n2. Создать сессию\n>'))
        
        if not os.path.exists('sessions'):
            os.mkdir('sessions')
        
        if action == 2:
            await create_sessions()

        if action == 1:
            accounts = await Accounts().get_accounts()
                    
            tasks = []
            with open('fake_info.txt','r') as file:
                fake_info = [i.strip() for i in file.readlines()]
            if USE_PROXY:
                proxy_dict = {}
                with open('proxy.txt','r',encoding='utf-8') as file:
                    proxy = [i.strip().split() for i in file.readlines() if len(i.strip().split()) == 2]
                    for prox,name in proxy:
                        proxy_dict[name] = prox
                for thread, account in enumerate(accounts):
                    if account in proxy_dict:
                        tasks.append(asyncio.create_task(Blum(account=account, thread=thread, proxy=proxy_dict[account],add_info=fake_info[thread]).main()))
                    else:
                        tasks.append(asyncio.create_task(Blum(account=account, thread=thread,proxy = None,add_info=fake_info[thread]).main()))
            else:
                for thread, account in enumerate(accounts):
                    tasks.append(asyncio.create_task(Blum(account=account, thread=thread,proxy = None,add_info=fake_info[thread]).main()))
            await asyncio.gather(*tasks)

    if __name__ == '__main__':
        asyncio.get_event_loop().run_until_complete(main())
