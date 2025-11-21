# League of Legends Auto Ready-Check Script

This script automatically finds your League of Legends installation,
reads the **lockfile**, and interacts with the local Riot client API to:

-   Detect match found\
-   Auto-accept ready checks\
-   Detect when the game starts

------------------------------------------------------------------------

## 🔧 Features

-   Automatically detects the game installation by scanning the running
    process.
-   Reads the lockfile to extract authentication token and port.
-   Uses Riot LCU API to check ready-check state and accept matches.
-   Checks if you are already in-game.

------------------------------------------------------------------------

## 📦 Requirements

Install dependencies:

``` bash
pip install aiohttp psutil
```

------------------------------------------------------------------------

## ▶️ How to Use

1.  Ensure **LeagueClientUx.exe** is running.
2.  Run the script with Python:

``` bash
python auto_accept.py
```

3.  The script will:
    -   Locate the lockfile automatically\
    -   Start monitoring matchmaking\
    -   Auto-accept matches

------------------------------------------------------------------------

## ⚠️ Disclaimer

This script interacts with Riot's local client API.\
Use at your own risk. It may violate Riot's terms depending on use.

------------------------------------------------------------------------

## 📁 File Structure Example

    auto_accept.py
    README.md

------------------------------------------------------------------------

Enjoy automating your ready-check!
