from dataclasses import dataclass, field


@dataclass
class Company:
    id: int
    name: str
    baseUrl: str
    searchPath: str
    searchQuery: str
    paginationType: str | None = None
    urlAttributeType: str = "href"
    xpaths: dict[str, str] = field(default_factory=dict)

    def searchUrl(self) -> str:
        return self.baseUrl + self.searchPath + self.searchQuery