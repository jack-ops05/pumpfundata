import asyncio
import json
from listener import listener
import states
from telegram_alert import send_alert
import websockets

async def connect_pumpportal():

    URI = 'wss://pumpportal.fun/api/data'
    initial_connection = True

    while True:
        #Subscribe to new tokens
        async with websockets.connect(URI) as ws:
            await ws.send(json.dumps({'method': 'subscribeNewToken'}))
            if initial_connection is False:
                await send_alert(msg='🟩 ALERT: Reconnected to websocket')
            await listener(ws)

        #Clean up/Reconnect
        for mint in states.token_tasks.values():
            task = mint['task']
            task.cancel()
        states.token_tasks.clear()
        initial_connection = False
        await asyncio.sleep(5)
