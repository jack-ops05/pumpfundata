import asyncio
import json
from listener import listener
import logging
import states
import websockets

LOG = logging.getLogger('main')

async def connect_pumpportal():

    URI = 'wss://pumpportal.fun/api/data'

    while True:
        try:
            async with websockets.connect(URI) as ws:
                payload = {'method': 'subscribeNewToken'}
                await ws.send(json.dumps(payload))
                LOG.info('Pumpportal websocket successfully connected')
                await listener(ws)

        except Exception as ex:
            for task in states.tracking_tasks:
                task.cancel()
            states.token_queues.clear()
            LOG.error(f'Pumpportal websocket connection failed // Exception: {ex}')
            await asyncio.sleep(3)
