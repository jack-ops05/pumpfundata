from datetime import datetime
from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from fastapi.responses import StreamingResponse
import json
import logging
import os
import psycopg2

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')
LOG = logging.getLogger('main')

app = FastAPI()

def connect_to_database():
    try:
        conn = psycopg2.connect(
            dbname=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT')
        )
        LOG.info('Connected to database')
        return conn
    except Exception as ex:
        LOG.error(f'Failed to connect to database // Exception: {ex}')
        return None

@app.get('/getEvents')
def get_events(start, end):

    LOG.info('Recieved GET request for /getEvents')

    try:
        start = datetime.fromisoformat(start)
        end = datetime.fromisoformat(end)
    except ValueError:
        raise HTTPException(status_code=400, detail='Invalid datetime format. Use ISO YYYY-MM-DDTHH:MM:SS')

    conn = connect_to_database()
    if conn is None:
        raise HTTPException(status_code=500, detail='Failed to connect to database')

    cur = conn.cursor(name='stream_cursor')
    cur.itersize = 1000

    try:
        cur.execute('SELECT row_to_json(events) FROM events WHERE timestamp BETWEEN %s AND %s ORDER BY timestamp ASC', (start, end))

        def stream_events():
            try:
                for row in cur:
                    yield json.dumps(row[0], default=str) + '\n'
            finally:
                cur.close()
                conn.close()

        return StreamingResponse(stream_events(), media_type='application/x-ndjson')

    except Exception as ex:
        cur.close()
        conn.close()
        LOG.error(f'Stream setup failed: {ex}')
        raise HTTPException(status_code=502, detail='StreamingResponse failed')
