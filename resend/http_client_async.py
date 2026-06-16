from abc import ABC, abstractmethod
from typing import Any, Dict, List, Mapping, Optional, Tuple, Union


class AsyncHTTPClient(ABC):
    """
    Abstract base class for async HTTP clients.
    This class defines the interface for making async HTTP requests.
    Subclasses should implement the `request` method.
    """

    @abstractmethod
    async def request(
        self,
        method: str,
        url: str,
        headers: Mapping[str, str],
        json: Optional[Union[Dict[str, object], List[object]]] = None,
        files: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, str]] = None,
    ) -> Tuple[bytes, int, Mapping[str, str]]:
        pass
