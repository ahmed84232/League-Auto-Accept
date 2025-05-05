import time

from aiohttp import ClientSession
import asyncio
import base64

lockfile_location = "C:\Partition\Games\Riot Games\League of Legends\lockfile"
with open(lockfile_location, "r") as f:
    data = f.read().split(":")
    port = data[2]
    token = data[3]
    print(token)
    riot_token = f"riot:{token}"
    riot_token = base64.b64encode(riot_token.encode()).decode()
    print(port, riot_token)

ready_check = f"https://127.0.0.1:{port}/lol-matchmaking/v1/ready-check"
accept_ready_check = f"https://127.0.0.1:{port}/lol-matchmaking/v1/ready-check/accept"

headers = {
    "Authorization": f"Basic {riot_token}",
    "Accept": "application/json"
}


async def main():
    async with ClientSession() as session:
        for i in range(1, 1000):

            async with session.get(ready_check, ssl=False, headers=headers) as response:

                print("Status:", response.status)
                html = await response.json()

                if "state" in html:
                    if html['state'] == 'Invalid':
                        print("Accept is not there yet...")
                        await asyncio.sleep(2)
                    elif html['state'] == 'InProgress':
                        print("MAAAAAATCHHHH FAAAAAOUUUUNNDDD!")
                        await session.post(accept_ready_check, ssl=False, headers=headers)
                        print("Accept button got Accepted ya walla")
                        await asyncio.sleep(50)
                        break

                else:
                    print("You didn't press find match yet...")
                    await asyncio.sleep(1)


asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(main())
