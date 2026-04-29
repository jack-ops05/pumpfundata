import asyncio
import json
from listener import listener
import logging
import states
from telegram_alert import send_alert
import websockets

LOG = logging.getLogger('main')

async def connect_pumpportal(httpxClient):

    URI = 'wss://pumpportal.fun/api/data'

    while True:
        try:
            async with websockets.connect(URI) as ws:
                await ws.send(json.dumps({'method': 'subscribeNewToken'}))
                LOG.info('Pumpportal websocket successfully connected')
                await send_alert(httpxClient, msg='🟩 ALERT: Pumpportal websocket connection successful...')
                await listener(httpxClient, ws)

        except Exception as ex:
            LOG.error(f'Pumpportal websocket connection failed | {ex}')

        for task in states.tracking_tasks.values():
            task.cancel()
        states.token_queues.clear()
        await asyncio.sleep(3)
        await send_alert(httpxClient, msg='🟨 ALERT: Pumpportal websocket reconnecting...')
