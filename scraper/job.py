from dataclasses import dataclass, field


@dataclass
class Job:
    url: str
    idCompany: int
    title: str
    jobDesc: str
    offices: str | None
    remote: str | None
    datePosted: str | None = None
    #Job(url, title, jobDesc, locations, remote, datePosted, idCompany)
    minSalary: int = -1
    maxSalary: int = -1
    minExperience: int = -1
    maxExperience: int = -1
    locations: list[str] = field(default_factory=dict)