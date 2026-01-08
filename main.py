import sys
import time
import os
from aiohttp import ClientSession
import asyncio
import base64
import psutil


def find_lol_by_process_scan():

    client_process_name = "LeagueClientUx.exe"
    for proc in psutil.process_iter(['name', 'exe']):

        if proc.info['name'] == client_process_name:

            exe_path = proc.info['exe']
            install_folder = os.path.dirname(exe_path)
            lockfile = os.path.join(install_folder, "lockfile")

            print(f"Found installation via process scan: {install_folder} \n")
            return lockfile

    print("LeagueClientUx.exe process not found.")
    return find_lol_by_process_scan()

lockfile_location = find_lol_by_process_scan()

with open(lockfile_location, "r") as f:
    data = f.read().split(":")
    port = data[2]
    token = data[3]
    riot_token = f"riot:{token}"
    riot_token = base64.b64encode(riot_token.encode()).decode()

ready_check = f"https://127.0.0.1:{port}/lol-matchmaking/v1/ready-check"
accept_ready_check = f"https://127.0.0.1:{port}/lol-matchmaking/v1/ready-check/accept"
game_flow_phase_check = f"https://127.0.0.1:{port}/lol-gameflow/v1/gameflow-phase"

headers = {
    "Authorization": f"Basic {riot_token}",
    "Accept": "application/json"
}


async def main():

    async with ClientSession() as session:

        for i in range(1, 1000):
            async with session.get(game_flow_phase_check, ssl=False, headers=headers) as phase_response:

                phase_text = await phase_response.text()
                os.system("cls")
                print("Current phase: " + phase_text.strip('"') + "\n")

                if "InProgress" in phase_text or "InGame" in phase_text:

                    print("Closing in 10 sec...")
                    time.sleep(10)
                    raise SystemExit

                if "ChampSelect" in phase_text:

                    time.sleep(5)
                    continue

            async with session.get(ready_check, ssl=False, headers=headers) as response:


                html = await response.json()

                if "state" in html:

                    if html['state'] == 'Invalid':

                        print("No Match found yet")
                        await asyncio.sleep(2)

                    elif html['state'] == 'InProgress':

                        print("Match Found")
                        await session.post(accept_ready_check, ssl=False, headers=headers)
                        print("Match got Accepted!")
                        await asyncio.sleep(5)

                else:

                    print("You didn't press find match yet...")
                    await asyncio.sleep(5)


asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(main())
