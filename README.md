# 🎮 League of Legends Auto-Accept Bot

A Python script that automatically accepts matchmaking when a match is found in League of Legends. The bot communicates directly with the League client's internal API using the `lockfile` for authentication.

---

## 📦 Requirements

- Python 3.7+
- `aiohttp` library

Install dependencies:

```bash
pip install aiohttp
```

---

## ⚙️ Setup

1. **Locate the `lockfile`**:
   - This file is typically found in the `C:\Partition\Games\Riot Games\League of Legends\lockfile` path.
   - It contains the port and token necessary to communicate with the League client.

2. **Update the `lockfile_location`** in the script if needed.

---

## 🚀 Usage

1. Open the League of Legends client.
2. Run the script:

```bash
python lol_auto_accept_bot.py
```

3. The script will:
   - Poll for a matchmaking `ready-check`.
   - Automatically accept the match once found.

---

## ⚠️ Warning

- **Only works on Windows** with the official Riot client.
- **Use responsibly**—automating actions may violate Riot's terms of service if misused.

---

## 📜 License

This project is open source and free for anyone to use or modify under the MIT License.
