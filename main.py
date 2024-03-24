import asyncio
import ctypes
import sys
import os

from core.autoreger import AutoReger
from core.backpack_trade import BackpackTrade
from art import tprint

from inputs.config import (THREADS, DELAY_BETWEEN_TRADE, DELAY_BETWEEN_DEAL,
                           ALLOWED_ASSETS, NEEDED_TRADE_VOLUME, MIN_BALANCE_TO_LEFT, TRADE_AMOUNT)

def read_file(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            content = file.read().strip()
        return content
    else:
        return ""

def get_environment_variable(key):
    return os.getenv(key, "")

def load_accounts():
    accounts_content = os.getenv("ACCOUNTS_FILE_CONTENT")
    if accounts_content:
        with open("inputs/accounts.txt", "w") as f:
            f.write(accounts_content)

def load_proxies():
    proxies_content = os.getenv("PROXIES_FILE_CONTENT")
    if proxies_content:
        with open("inputs/proxies.txt", "w") as f:
            f.write(proxies_content)

async def worker_task(account: str, proxy: str):
    api_key, api_secret = account.split(":")
    backpack = BackpackTrade(api_key, api_secret, proxy, DELAY_BETWEEN_TRADE, DELAY_BETWEEN_DEAL,
                             NEEDED_TRADE_VOLUME, MIN_BALANCE_TO_LEFT, TRADE_AMOUNT)

    await backpack.start_trading(pairs=ALLOWED_ASSETS)

    await backpack.close()

    return True


async def main():
    # bot_info("Backpack_Trading")

    autoreger = AutoReger.get_accounts(load_accounts(), load_proxies())
    await autoreger.start(worker_task, THREADS)


if __name__ == '__main__':
    asyncio.run(main())
