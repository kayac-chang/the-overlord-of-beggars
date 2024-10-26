from abc import ABC, abstractmethod
from typing import List

from app.models.geolocation import GeoLocation
from app.models.store import Store


class StoreSearchService(ABC):
    @abstractmethod
    async def get_stores_by_keyword_and_location(
        self, keyword: str, location: GeoLocation
    ) -> List[Store]:
        pass

    @abstractmethod
    async def get_stores_by_keyword(self, keyword: str) -> List[Store]:
        pass

    @abstractmethod
    async def get_stores_by_location(self, location: GeoLocation) -> List[Store]:
        pass

    @abstractmethod
    async def get_store_by_store_id(self, id: str) -> Store | None:
        pass

    @abstractmethod
    async def get_store_by_store_id_and_location(
        self, id: str, location: GeoLocation
    ) -> Store | None:
        pass
