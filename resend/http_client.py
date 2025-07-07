from abc import ABC, abstractmethod
from typing import Dict, List, Mapping, Optional, Tuple, Union


class HTTPClient(ABC):
    """
    Abstract base class for HTTP clients.
    This class defines the interface for making HTTP requests.
    Subclasses should implement the `request` method.
    """

    @abstractmethod
    def request(
        self,
        method: str,
        url: str,
        headers: Mapping[str, str],
        json: Optional[Union[Dict[str, object], List[object]]] = None,
    ) -> Tuple[bytes, int, Mapping[str, str]]:
        pass
