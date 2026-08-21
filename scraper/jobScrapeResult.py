from dataclasses import dataclass
from scraper.job import Job
from scraper.company import Company


@dataclass
class JobScrapeResult:
    job: Job | None
    company: Company

    def __str__(self):
        if not self.job:
            return f'{self.company.name}: None'
        
        return f'{self.company.name}: {self.job.title}'