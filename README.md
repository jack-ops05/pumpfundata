# Pump.fun Data Collector

## Description:
A simple Python script that utilizes the pumpportal websocket to get creation and trade events from the pump.fun smart contract. The script filters out certain coins such as bonk 
launches and mayhem mode launches, in other words, only tokens where the pool == "pump" and is_mayhem_mode is False, are tracked. Coins are tracked for a minimum of 90 seconds and
a maximum of 600 seconds (10 minutes). If no trade events occur on a coin within 90 seconds, the token is basically dead and the tracker will be closed. On close of the tracker, all
coin data including the creation event and trade events will be inserted into the PostgreSQL database in the "postgres" Docker container. Thank you for using my repo and if you
found it helpful, a star is much appreciated. Im a beginner Python dev and have been coding for >1 year, therefore if you find any bugs or have any ideas, sharing them is also much
appreciated. 

-Jack

## How to use:
1. Rent a cloud server
2. Install Docker & Docker Compose on server (sudo apt install docker.io docker-compose)
3. Clone this repository on server
4. Change directories (cd pumpfundata)
5. Build containers (docker compose up -d --build)
6. Run (docker ps) to verify containers are up and running
7. Done

## Pulling the data:
You can easily pull data from anywhere using the FastAPI and Uvicorn setup in the Docker container "api". The script utilizes the FastAPI StreamingResponse class to reduce any errors
pulling large amounts of data. Here is a copy and paste script you can use to pull data. 

```python
import requests
import json

url = "http://your_server_ip:8000/getEvents"
params = {
    "start": "2026-04-28T00:00:00",
    "end": "2026-04-28T23:59:59"
}

with requests.get(url, params=params, stream=True) as r:
    for line in r.iter_lines():
        if line:
            decoded = line.decode()
            data = json.loads(decoded)
            print(data) 
```

## Telegram Alerts
To set up Telegram alerts, 2 secret variables are needed. One, the bot token, two, the chat id. These variables are automatically set to None so Telegram alerts will by default not send unless you set it up. To set up Telegram alerts follow the instructions below:

1. Search @BotFather on Telegram
2. Send the message /newbot
3. Configure name and username for bot, then copy the bot token
4. Send a test message to the bot
5. Open your browser and look up https://api.telegram.org/your_bot_token/getUpdates
6. Look for the 'id' key and copy the value, this is your chat id
7. Go to the docker-compose.yml file and under the "collector" container, change the enviroment variables TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID
8. Done
