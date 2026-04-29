import asyncio
from database import db_listener
import httpx
import logging
from pumpportal import connect_pumpportal

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')
LOG = logging.getLogger('main')

async def main():
    async with httpx.AsyncClient() as httpxClient:
        asyncio.create_task(db_listener(httpxClient))
        await connect_pumpportal(httpxClient)

if __name__ == '__main__':
    try:
        LOG.info('Starting program')
        asyncio.run(main())
    except KeyboardInterrupt:
        LOG.info('Stopping program')
