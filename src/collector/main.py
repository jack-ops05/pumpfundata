import asyncio
import logging
from pumpportal import connect_pumpportal

logging.basicConfig(level=logging.WARNING, format='%(asctime)s | %(levelname)s | %(message)s')
LOG = logging.getLogger('main')

async def main():
    await connect_pumpportal()

if __name__ == '__main__':
    try:
        LOG.info('Starting program')
        asyncio.run(main())
    except KeyboardInterrupt:
        LOG.info('Stopping program')
