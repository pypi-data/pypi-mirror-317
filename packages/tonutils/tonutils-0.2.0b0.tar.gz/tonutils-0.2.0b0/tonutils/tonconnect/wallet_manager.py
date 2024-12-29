import json
from pathlib import Path
from typing import Any, Dict, List, Optional

import aiohttp
from cachetools import TTLCache

from .exceptions import FetchWalletsError
from .models.wallet import WalletApp


class FallbackWalletManager:
    FILE_PATH = Path(__file__).parent / "_data/fallback_wallets.json"

    @staticmethod
    def load_wallets() -> List[Dict[str, Any]]:
        if not FallbackWalletManager.FILE_PATH.exists():
            FallbackWalletManager.save_wallets([])
            return []
        with open(FallbackWalletManager.FILE_PATH, "r") as file:
            return json.load(file)

    @staticmethod
    def save_wallets(wallets: List[Dict[str, Any]]) -> None:
        FallbackWalletManager.FILE_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(FallbackWalletManager.FILE_PATH, "w", encoding="utf-8") as file:
            file.write(json.dumps(wallets, indent=4))


class CachedWalletManager:

    def __init__(self, cache_ttl: Optional[int] = None) -> None:
        if cache_ttl is None:
            cache_ttl = 86400
        self.cache: TTLCache = TTLCache(maxsize=1, ttl=cache_ttl)

    def get_wallets(self) -> Optional[List[Dict[str, Any]]]:
        return self.cache.get("wallets")

    def save_wallets(self, wallets: List[Dict[str, Any]]) -> None:
        self.cache["wallets"] = wallets


class WalletsListManager:
    DEFAULT_URL = "https://raw.githubusercontent.com/ton-blockchain/wallets-list/main/wallets-v2.json"

    def __init__(
            self,
            source_url: Optional[str] = None,
            include_wallets: Optional[List[str]] = None,
            exclude_wallets: Optional[List[str]] = None,
            cache_ttl: Optional[int] = None,
    ) -> None:
        self._cache_manager = CachedWalletManager(cache_ttl)
        self._fallback_manager = FallbackWalletManager()

        self.include_wallets = set(include_wallets or [])
        self.exclude_wallets = set(exclude_wallets or [])
        self.source_url = source_url or WalletsListManager.DEFAULT_URL

    async def _fetch_wallets(self) -> List[Dict[str, Any]]:
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(self.source_url) as response:
                    response.raise_for_status()
                    content = await response.text()
                    wallets = json.loads(content)
                    if not isinstance(wallets, list):
                        raise FetchWalletsError("Invalid format: expected a list of wallets.")
                    return wallets
            except aiohttp.ClientError as e:
                raise FetchWalletsError(f"Error fetching wallets: {e}")
            except Exception as e:
                raise FetchWalletsError(f"Unexpected error: {e}")

    def _filter_wallets(self, wallets: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        filtered_wallets = [
            w for w in wallets if w["app_name"] not in self.exclude_wallets
        ]
        if self.include_wallets:
            filtered_wallets = [
                w for w in filtered_wallets if w["app_name"] in self.include_wallets
            ]
        return filtered_wallets

    @staticmethod
    def _get_supported_wallets(wallets: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        supported_wallets = []
        for wallet in wallets:
            for bridge in wallet.get("bridge", []):
                if bridge.get("type") == "sse" and "url" in bridge:
                    wallet_copy = wallet.copy()
                    wallet_copy["bridge_url"] = bridge["url"]
                    supported_wallets.append(wallet_copy)
                    break
        return supported_wallets

    def _save_wallets(self, wallets: List[Dict[str, Any]]) -> None:
        self._cache_manager.save_wallets(wallets)
        self._fallback_manager.save_wallets(wallets)

    async def get_wallets(self) -> List[WalletApp]:
        cached_wallets = self._cache_manager.get_wallets()
        if cached_wallets is None:
            try:
                remote_wallets = await self._fetch_wallets()
            except FetchWalletsError:
                remote_wallets = self._fallback_manager.load_wallets()
            self._save_wallets(remote_wallets)
            wallets_to_return = remote_wallets
        else:
            wallets_to_return = cached_wallets

        filtered_wallets = self._filter_wallets(wallets_to_return)
        supported_wallets = self._get_supported_wallets(filtered_wallets)
        return [WalletApp.from_dict(w) for w in supported_wallets]
