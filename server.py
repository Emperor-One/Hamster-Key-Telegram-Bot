import asyncio
import os
import sys
import httpx
import random
import time
import uuid
import datetime
from loguru import logger

# Disable logging for httpx
httpx_log = logger.bind(name="httpx").level("WARNING")
logger.remove()
logger.add(sink=sys.stdout, format="<white>{time:YYYY-MM-DD HH:mm:ss}</white>"
                                   " | <level>{level: <8}</level>"
                                   " | <cyan><b>{line}</b></cyan>"
                                   " - <white><b>{message}</b></white>")
logger = logger.opt(colors=True)

GAMES = {
    1: {
        'name': 'Riding Extreme 3D',
        'appToken': 'd28721be-fd2d-4b45-869e-9f253b554e50',
        'promoId': '43e35910-c168-4634-ad4f-52fd764a843f',
    },
    2: {
        'name': 'My Clone Army',
        'appToken': '74ee0b5b-775e-4bee-974f-63e7f4d5bacb',
        'promoId': 'fe693b26-b342-4159-8808-15e3ff7f8767',
    },
    3: {
        'name': 'Chain Cube 2048',
        'appToken': 'd1690a07-3780-4068-810f-9b5bbf2931b2',
        'promoId': 'b4170868-cef0-424f-8eb9-be0622e8e8e3',
    },
    4: {
        'name': 'Train Miner',
        'appToken': '82647f43-3f87-402d-88dd-09a90025313f',
        'promoId': 'c4480ac7-e178-4973-8061-9ed5b2e17954',
    }
}

BASE_URL = 'https://api.gamepromo.io'
EVENTS_DELAY = 30
HTTPX_TIMEOUT = 30

key_count = 0

async def login(client_id, app_token):
    headers = {
        "User-Agent": "UnityPlayer/2022.3.20f1 (UnityWebRequest/1.0, libcurl/8.5.0-DEV)",
        "Connection": "close"
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f'{BASE_URL}/promo/login-client',
            headers=headers,
            json={'appToken': app_token, 'clientId': client_id, 'clientOrigin': 'android'},
            timeout=httpx.Timeout(HTTPX_TIMEOUT)  
        )
        response.raise_for_status()
        client_token = response.json()['clientToken']
        logger.info(f"Logged in with Client Token: {client_token}")

        return client_token

async def register_event(client_token, promo_id):
    headers = {
        "Authorization": f"Bearer {client_token}",
        "User-Agent": "UnityPlayer/2022.3.20f1 (UnityWebRequest/1.0, libcurl/8.5.0-DEV)",
        "Connection": "close"
    }
    async with httpx.AsyncClient() as client:
        while True:
            delay_time = EVENTS_DELAY * (random.uniform(0,0.33) + 1)
            logger.info(f"Sleeping for {delay_time} seconds.")
            await asyncio.sleep(delay_time)

            response = await client.post(
                f'{BASE_URL}/promo/register-event',
                headers=headers,
                json={'promoId': promo_id, 'eventId': str(uuid.uuid4()), 'eventOrigin': 'undefined'},
                timeout=httpx.Timeout(HTTPX_TIMEOUT)  
            )
            logger.info(f"Response received: {response.json()}")

            if 'hasCode' in response.json():
                break

        has_code = response.json()['hasCode']

        if has_code:
            logger.success("Code is ready!")
        else:
            logger.info("Code is not ready.")
        return has_code


async def create_code(client_token, promo_id):
    headers = {
        "Authorization": f"Bearer {client_token}",
        "User-Agent": "UnityPlayer/2022.3.20f1 (UnityWebRequest/1.0, libcurl/8.5.0-DEV)",
        "Connection": "close"
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f'{BASE_URL}/promo/create-code',
            headers=headers,
            json={'promoId': promo_id},
            timeout=httpx.Timeout(HTTPX_TIMEOUT)
        )
        response.raise_for_status()
        key = response.json()['promoCode']

        logger.success(f"Key Generated: {key}")
        return key


async def play_the_game(app_token, promo_id):
    client_id = str(uuid.uuid4())

    try:
        client_token = await login(client_id, app_token)

    except Exception as e:
        logger.error(f"Failed to login: {e}")
        return None

    try:
        has_code = await register_event(client_token, promo_id)

    except Exception as e:
        return None

    try:
        key = await create_code(client_token, promo_id)
        return key

    except Exception as e:
        logger.error(f"An error occured while trying to create the code: {e}")
        return None

async def main(chosen_game, no_of_keys):
    tasks = [play_the_game(GAMES[chosen_game]['appToken'], GAMES[chosen_game]['promoId']) for _ in range(no_of_keys)]
    keys = await asyncio.gather(*tasks)
    return [key for key in keys if key]


# Call run directly if you are a bot
async def run(chosen_game, no_of_keys):
    if no_of_keys == 1:
        logger.info(f"Generating {no_of_keys} key for {GAMES[chosen_game]['name']}")
    else:
        logger.info(f"Generating {no_of_keys} keys for {GAMES[chosen_game]['name']}")

    keys = await main(chosen_game=chosen_game, no_of_keys=no_of_keys)    
    return keys
    
if __name__ == "__main__":
    print("Select a game:")
    for key, value in GAMES.items():
        print(f"{key}: {value['name']}")
    chosen_game = int(input("Enter the game number: "))
    no_of_keys = int(input("Enter the number of keys to generate: "))

    if no_of_keys == 1:
        logger.info(f"Generating {no_of_keys} key for {GAMES[chosen_game]['name']}")
    else:
        logger.info(f"Generating {no_of_keys} keys for {GAMES[chosen_game]['name']}")
   
    keys = asyncio.run(main(chosen_game, no_of_keys))

    if keys:
        with open('Keys.txt', 'a') as file:  
            for key in keys:
                file.write(f"{key}\n")
            logger.success("Generated Key(s) were successfully saved to Keys.txt")

    else:
        logger.error("No keys were generated.")    

    input("Press Any Key To Exit")
