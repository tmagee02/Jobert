package com.jobert.backendSB.Job.mapper;

import java.util.function.Function;

import org.springframework.stereotype.Component;

import com.jobert.backendSB.Job.Job;
import com.jobert.backendSB.Job.dto.JobDetailsDTO;

@Component
public class JobDetailsDTOMapper implements Function<Job, JobDetailsDTO> {

    @Override
    public JobDetailsDTO apply(Job job) {
        return new JobDetailsDTO(
            job.getCompany().getCompanyName(),
            job.getJobUrl(),
            job.getTitle(),
            job.getJobDesc(),
            job.getMinExperience(),
            job.getMaxExperience(),
            job.getMinSalary(),
            job.getMaxSalary(),
            job.getDateScraped()
        );
    }

}
