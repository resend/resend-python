from abc import ABC, abstractmethod
from typing import Mapping, Optional, Tuple, Union, List


class HTTPClient(ABC):
    @abstractmethod
    def request(
        self,
        method: str,
        url: str,
        headers: Mapping[str, str],
        json: Optional[Union[dict[str, object], List[object]]] = None,
    ) -> Tuple[bytes, int, Mapping[str, str]]:
        pass
