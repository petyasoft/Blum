import asyncio
from data.config import NODE_PATH

async def get_payload(gameId, points, freeze):

    process = await asyncio.create_subprocess_exec(
        NODE_PATH, 
        'utils/payload/blum.mjs', 
        gameId, 
        str(points),
        str(freeze),
        stdout=asyncio.subprocess.PIPE,
        )
    output, _ = await process.communicate()
    payload = output.decode('utf-8').strip()
    return payload

