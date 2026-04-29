import asyncpg
import logging
import os
from telegram_alert import send_alert

LOG = logging.getLogger('main')

async def insert_data(data):

    try:
        #Connect to database
        conn = await asyncpg.connect(
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        )

        await conn.executemany(
                '''
                INSERT INTO events (signature, mint, timestamp, txType, traderKey, curveKey, solAmount, tokenAmount, vSol, vTokens, marketCap)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
                ''',
                data
            )
        await conn.close()

    except Exception as ex:
        LOG.error(f'Database insertion error | {ex}')
        await send_alert(msg='🟥 ALERT: Database insertion failed')
