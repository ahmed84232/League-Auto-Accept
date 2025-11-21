import time
import os
from aiohttp import ClientSession
import asyncio
import base64
import psutil

# You would need to install this library: pip install psutil
def find_lol_by_process_scan():
    """
    Scans running processes for 'LeagueClientUx.exe' to determine the path.
    """
    # The lockfile is created by the UX process
    client_process_name = "LeagueClientUx.exe"

    for proc in psutil.process_iter(['name', 'exe']):
        if proc.info['name'] == client_process_name:
            # The 'exe' field contains the full path to the running executable
            exe_path = proc.info['exe']

            # The lockfile is in the parent directory of the executable
            install_folder = os.path.dirname(exe_path)
            lockfile = os.path.join(install_folder, "lockfile")

            print(f"Found installation via process scan: {install_folder}")
            return lockfile

    print("LeagueClientUx.exe process not found.")
    return "None"

lockfile_location = find_lol_by_process_scan()

with open(lockfile_location, "r") as f:
    data = f.read().split(":")
    port = data[2]
    token = data[3]
    riot_token = f"riot:{token}"
    riot_token = base64.b64encode(riot_token.encode()).decode()

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


                html = await response.json()

                if "state" in html:

                    if html['state'] == 'Invalid':

                        print("state == "+ html['state'])
                        print("Accept is not there yet...")
                        print("Status:", response.status)
                        await asyncio.sleep(2)

                    elif html['state'] == 'InProgress':

                        print("MAAAAAATCHHHH FAAAAAOUUUUNNDDD!")
                        await session.post(accept_ready_check, ssl=False, headers=headers)
                        print("Accept button got Accepted ya walla")
                        await asyncio.sleep(5)

                else:

                    os.system("cls")
                    print("You didn't press find match yet...")
                    await asyncio.sleep(1)


asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(main())
