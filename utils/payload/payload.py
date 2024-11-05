import asyncio
import platform
from data.config import NODE_PATH
async def get_payload(gameId, points):

    is_linux = platform.system().lower() == 'linux'

    if is_linux:
        process = await asyncio.create_subprocess_exec('which', 'node', stdout=asyncio.subprocess.PIPE)
        output, _ = await process.communicate()
        node_path = output.decode('utf-8').strip()
    else:
        node_path = 'node'

    process = await asyncio.create_subprocess_exec(NODE_PATH, 'utils/payload/blum.mjs', gameId, str(points), stdout=asyncio.subprocess.PIPE)
    output, _ = await process.communicate()
    payload = output.decode('utf-8').strip()
    return payload