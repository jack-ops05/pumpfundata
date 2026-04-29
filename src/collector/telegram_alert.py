import httpx
import os

async def send_alert(msg):
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')

    if bot_token == 'None':
        return
    if chat_id == 'None':
        return

    async with httpx.AsyncClient() as client:
        url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
        payload = {'chat_id': f'{chat_id}', 'text': msg}
        await client.post(url, json=payload)
