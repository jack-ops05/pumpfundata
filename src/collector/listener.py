import asyncio
from datetime import datetime, timezone
import json
import logging
import states
from tracker import track_mint

LOG = logging.getLogger('main')

async def listener(ws):

    while True:
        try:
            msg = await ws.recv()
            data = json.loads(msg)

            data['timestamp'] = datetime.now(timezone.utc)
            mint = data.get('mint')
            tx_type = data.get('txType')

            if mint is None:
                continue

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
        except Exception as ex:
            LOG.error(f'Listener error // Exception: {ex}')
