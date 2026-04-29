import asyncio
from datetime import datetime, timezone
import json
import logging
import states
from telegram_alert import send_alert
from tracker import track_mint
import websockets

LOG = logging.getLogger('main')

async def listener(httpxClient, ws):

    while True:
        try:
            msg = await ws.recv()
            data = json.loads(msg)

            mint = data.get('mint')
            if mint is None:
                continue

            data['timestamp'] = datetime.now(timezone.utc)
            tx_type = data['txType']

            if tx_type == 'create':
                pool = data['pool']
                if pool == 'pump':
                    is_mayhem_mode = data['is_mayhem_mode']
                    if is_mayhem_mode is False:
                        states.tracking_tasks[mint] = asyncio.create_task(track_mint(ws, data))
                        states.token_queues[mint] = asyncio.Queue()
                        LOG.info(f'Tracking [{len(states.token_queues)}] tokens')

            if tx_type in ['buy', 'sell']:
                queue = states.token_queues[mint]
                await queue.put(data)

        except websockets.exceptions.ConnectionClosedOK:
            LOG.info('Websocket closed normally')
            await send_alert(httpxClient, msg='🟥 ALERT: Pumpportal websocket closed gracefully')
            break

        except websockets.exceptions.ConnectionClosedError as ex:
            LOG.info(f'Websocket closed unexpectedly | {ex}')
            await send_alert(httpxClient, msg='🟥 ALERT: Pumpportal websocket closed unexpectedly')
            break

        except Exception as ex:
            LOG.error(f'Listener error | {ex}')
