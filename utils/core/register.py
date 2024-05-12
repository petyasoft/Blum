from loguru import logger
from data import config
import pyrogram


async def create_sessions():
    while True:
        session_name = input('Введите название сессии (для выхода нажмите Enter)\n')
        if not session_name:
            return

        session = pyrogram.Client(
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            name=session_name,
            workdir=config.WORKDIR,
        )

        async with session:
            user_data = await session.get_me()

        logger.success(f'Добавлена сессия +{user_data.phone_number} @{user_data.username}')
