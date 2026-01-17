import os
import base64
import asyncio
import psutil
from aiohttp import ClientSession
from PySide6.QtCore import QThread, Signal


class AutoAcceptWorker(QThread):

    # Signals to update GUI
    log_signal = Signal(str, str)  # message, level
    phase_signal = Signal(str)
    connected_signal = Signal(bool)
    match_accepted_signal = Signal()
    
    def __init__(self):
        super().__init__()
        self._running = False
    
    def stop(self):
        self._running = False

    def find_lol_by_process_scan(self):

        client_process_name = "LeagueClientUx.exe"
        for proc in psutil.process_iter(['name', 'exe']):
            try:
                if proc.info['name'] == client_process_name:
                    exe_path = proc.info['exe']
                    install_folder = os.path.dirname(exe_path)
                    lockfile = os.path.join(install_folder, "lockfile")
                    return lockfile
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        return None
    
    def run(self):

        self._running = True
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            loop.run_until_complete(self.main())
        finally:
            loop.close()
    
    async def main(self):

        while self._running:
            # Find lockfile
            lockfile_location = self.find_lol_by_process_scan()
            
            if not lockfile_location or not os.path.exists(lockfile_location):
                self.log_signal.emit("LeagueClientUx.exe process not found.", "warning")
                self.connected_signal.emit(False)
                self.phase_signal.emit("Searching...")
                await asyncio.sleep(3)
                continue
            
            try:
                # Read lockfile
                with open(lockfile_location, "r") as f:
                    data = f.read().split(":")
                    port = data[2]
                    token = data[3]
                    riot_token = f"riot:{token}"
                    riot_token = base64.b64encode(riot_token.encode()).decode()
                
                # Build URLs
                ready_check = f"https://127.0.0.1:{port}/lol-matchmaking/v1/ready-check"
                accept_ready_check = f"https://127.0.0.1:{port}/lol-matchmaking/v1/ready-check/accept"
                game_flow_phase_check = f"https://127.0.0.1:{port}/lol-gameflow/v1/gameflow-phase"
                
                headers = {
                    "Authorization": f"Basic {riot_token}",
                    "Accept": "application/json"
                }
                
                self.log_signal.emit(f"Found installation: {os.path.dirname(lockfile_location)}", "success")
                self.connected_signal.emit(True)
                
                async with ClientSession() as session:
                    # ORIGINAL LOOP STRUCTURE
                    for i in range(1, 1000):
                        if not self._running:
                            break
                        
                        try:
                            async with session.get(game_flow_phase_check, ssl=False, headers=headers) as phase_response:
                                phase_text = await phase_response.text()
                                phase = phase_text.strip('"')
                                self.phase_signal.emit(phase)
                                
                                if "InProgress" in phase_text or "InGame" in phase_text:
                                    self.log_signal.emit("Game in progress...", "info")
                                    await asyncio.sleep(10)
                                    continue
                                
                                if "ChampSelect" in phase_text:
                                    await asyncio.sleep(5)
                                    continue
                            
                            async with session.get(ready_check, ssl=False, headers=headers) as response:
                                html = await response.json()
                                
                                if "state" in html:
                                    if html['state'] == 'Invalid':
                                        self.log_signal.emit("No Match found yet", "info")
                                        await asyncio.sleep(2)
                                    
                                    elif html['state'] == 'InProgress':
                                        self.log_signal.emit("Match Found", "success")
                                        await session.post(accept_ready_check, ssl=False, headers=headers)
                                        self.log_signal.emit("Match got Accepted!", "success")
                                        self.match_accepted_signal.emit()
                                        await asyncio.sleep(5)
                                else:
                                    self.log_signal.emit("You didn't press find match yet...", "info")
                                    await asyncio.sleep(5)
                        
                        except Exception as e:
                            self.log_signal.emit(f"Error: {str(e)[:50]}", "error")
                            break
                            
            except Exception as e:
                self.log_signal.emit(f"Error: {str(e)[:50]}", "error")
                self.connected_signal.emit(False)
                await asyncio.sleep(3)
        
        self.connected_signal.emit(False)
        self.phase_signal.emit("Stopped")
