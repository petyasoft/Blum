import subprocess
import asyncio

async def get_payload(gameId, points):
    process = await asyncio.create_subprocess_exec('node', 'utils/payload/blum.mjs', gameId, str(points), stdout=asyncio.subprocess.PIPE)
    output, _ = await process.communicate()
    payload = output.decode('utf-8').strip()
    return payload

