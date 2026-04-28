import asyncio
token_queues = {}
tracking_tasks = {}
database_queue = asyncio.Queue()
