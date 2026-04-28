import asyncio
import json
import logging
import states

LOG = logging.getLogger('main')

async def track_mint(ws, creation_data):

    try:
        mint = creation_data['mint']
        queue = states.token_queues[mint]
        data = [(
            creation_data['signature'],
            creation_data['mint'],
            creation_data['timestamp'],
            creation_data['txType'],
            creation_data['traderPublicKey'],
            creation_data['bondingCurveKey'],
            creation_data['solAmount'],
            creation_data['initialBuy'],
            creation_data['vSolInBondingCurve'],
            creation_data['vTokensInBondingCurve'],
            creation_data['marketCapSol']
        )]

        payload = {
            'method': 'subscribeTokenTrade',
            'keys': [mint]
        }
        await ws.send(json.dumps(payload))

        token_launch_time = asyncio.get_event_loop().time()

        while asyncio.get_event_loop().time() - token_launch_time < 600:

            try:
                trade_data = await asyncio.wait_for(queue.get(), timeout=90)
                data.append((
                    trade_data['signature'],
                    trade_data['mint'],
                    trade_data['timestamp'],
                    trade_data['txType'],
                    trade_data['traderPublicKey'],
                    trade_data['bondingCurveKey'],
                    trade_data['solAmount'],
                    trade_data['tokenAmount'],
                    trade_data['vSolInBondingCurve'],
                    trade_data['vTokensInBondingCurve'],
                    trade_data['marketCapSol']
                ))

            except asyncio.TimeoutError:
                break

        #Cleanup
        payload = {
            'method': 'unsubscribeTokenTrade',
            'keys': [mint]
        }
        await ws.send(json.dumps(payload))
        del states.token_queues[mint]
        await states.database_queue.put(data)

        LOG.info(f'Token task complete // Mint: {mint}')
        del states.tracking_tasks[mint]

    except Exception as ex:
        LOG.error(f'Tracker error // Exception: {ex}')
