from abc import ABC, abstractmethod
from typing import Any, Mapping, Optional, Tuple, Union


class HTTPClient(ABC):
    @abstractmethod
    def request(
        self,
        method: str,
        url: str,
        headers: Mapping[str, str],
        json: Optional[Union[dict, list]] = None,
    ) -> Tuple[bytes, int, Mapping[str, str]]:
        pass
