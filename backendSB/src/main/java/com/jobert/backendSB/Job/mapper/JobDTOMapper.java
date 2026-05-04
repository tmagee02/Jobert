package com.jobert.backendSB.Job.mapper;

import java.util.function.Function;

import org.springframework.stereotype.Component;

import com.jobert.backendSB.Job.Job;
import com.jobert.backendSB.Job.dto.JobDTO;

@Component
public class JobDTOMapper implements Function<Job, JobDTO> {

    @Override
    public JobDTO apply(Job job) {
        return new JobDTO(
            job.getJobId(),
            job.getJobUrl(),
            job.getCompany().getCompanyName(),
            job.getTitle(),
            job.getMinExperience(),
            job.getMaxExperience(),
            job.getMinSalary(),
            job.getMaxSalary(),
            job.getDateScraped()
        );
    }

}
