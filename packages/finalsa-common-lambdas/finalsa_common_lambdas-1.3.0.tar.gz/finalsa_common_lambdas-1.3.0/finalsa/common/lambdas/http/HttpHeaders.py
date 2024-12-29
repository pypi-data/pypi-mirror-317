from typing import Optional, Dict

class HttpHeaders():

    def __init__(self, headers: Dict[str, str]) -> None:
        self.headers = headers

    def get(self, key: str, default: Optional[str] = None) -> Optional[str]:
        return self.headers.get(key, default)

    def get_content_type(self) -> Optional[str]:
        return self.get("Content-Type", "")
