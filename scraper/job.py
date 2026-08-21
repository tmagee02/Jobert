from dataclasses import dataclass, field


@dataclass
class Job:
    url: str
    idCompany: int
    company: str
    title: str
    jobDesc: str
    offices: str | None
    remote: str | None
    datePosted: str | None = None
    minSalary: int = -1
    maxSalary: int = -1
    minExperience: int = -1
    maxExperience: int = -1
    locations: list[str] = field(default_factory=dict)


    def __str__(self):
        return f'{self.title[:10]} ({self.idCompany}) - {self.jobDesc[:3]}'