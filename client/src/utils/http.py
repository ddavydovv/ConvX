from aiogram.client.session import aiohttp


async def fetch_url(url, payload, headers):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload, headers=headers, ssl=False) as response:
            if response.status == 200:
                return await response.json()
            else:
                return None