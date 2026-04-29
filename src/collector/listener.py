import asyncio
from datetime import datetime, timezone
import json
import logging
import states
from telegram_alert import send_alert
from tracker import track_mint
import websockets

LOG = logging.getLogger('main')

async def listener(ws):

    while True:
        try:
            #Wait for messages
            msg = await ws.recv()
            data = json.loads(msg)

            mint = data.get('mint')
            if mint is None:
                continue

            data['timestamp'] = datetime.now(timezone.utc)

            tx_type = data['txType']

            #New token creation
            if tx_type == 'create':

                #Safeguard websocket duplication errors
                if mint in states.token_tasks:
                    LOG.warning('Duplicate create message detected')
                    continue

                #Conditions for token
                pool = data['pool']
                if pool == 'pump':
                    mayhem_mode = data['is_mayhem_mode']
                    if mayhem_mode is False:

                        #Subscribe to/Track token
                        states.token_tasks[mint] = {'task': asyncio.create_task(track_mint(ws, data)), 'queue': asyncio.Queue()}

            #Route trade data
            elif tx_type in ['buy', 'sell']:
                if mint not in states.token_tasks:
                    continue
                queue = states.token_tasks[mint]['queue']
                await queue.put(data)

        except websockets.exceptions.ConnectionClosedOK as ex:
            LOG.warning(f'Websocket connection closed OK | {ex}')
            await send_alert(msg=f'🟥 ALERT: Websocket connection closed OK | {ex}')
            break

        except websockets.exceptions.ConnectionClosedError as ex:
            LOG.warning(f'Websocket connection closed ERROR | {ex}')
            await send_alert(msg=f'🟥 ALERT: Websocket connection closed ERROR | {ex}')
            break

        except Exception as ex:
            LOG.error(f'Listener error | {ex}')
