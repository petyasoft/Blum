from utils.core import create_sessions
from utils.telegram import Accounts
from utils.yescoin import Yescoin
from utils.blum import Blum
from data.config import hello,USE_PROXY
import asyncio


async def main():
    print(hello)
    action = int(input('Выберите действие:\n1. Начать сбор монет\n2. Создать сессию\n>'))

    if action == 2:
        await create_sessions()

    if action == 1:
        accounts = await Accounts().get_accounts()
        with open('proxy.txt','r') as file:
            proxy = [i.strip() for i in file.readlines()]
        tasks = []
        if USE_PROXY:
            for thread, account in enumerate(accounts):
                if len(proxy) > thread:
                    tasks.append(asyncio.create_task(Blum(account=account, thread=thread, proxy=proxy[thread]).main()))
                else:
                    tasks.append(asyncio.create_task(Blum(account=account, thread=thread,proxy = None).main()))
        else:
            for thread, account in enumerate(accounts):
                tasks.append(asyncio.create_task(Blum(account=account, thread=thread,proxy = None).main()))
        await asyncio.gather(*tasks)



if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())

