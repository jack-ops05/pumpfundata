import asyncio
import asyncpg
import logging
import os
import states
from telegram_alert import send_alert

LOG = logging.getLogger('main')

async def db_listener(httpxClient):

    await asyncio.sleep(30)

    db_connection = await asyncpg.connect(
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')
    )
    LOG.info('Connected to PostgreSQL')
    queue = states.database_queue

    while True:
        try:

            data = await queue.get()
            await db_connection.executemany(
                'INSERT INTO events (signature, mint, timestamp, txType, traderKey, curveKey, solAmount, tokenAmount, vSol, vTokens, marketCap) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)',
                data
                )
            LOG.info('Inserted token into table')
        except Exception as ex:
            LOG.error(f'DB insertion error // Exception: {ex}')
            await send_alert(httpxClient, msg='🟥 ALERT: Database insertion failed')
