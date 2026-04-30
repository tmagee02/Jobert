package com.jobert.backendSB.Job;

import java.util.function.Function;

import org.springframework.stereotype.Component;

@Component
public class JobDTOMapper implements Function<Job, JobDTO> {

    @Override
    public JobDTO apply(Job job) {
        return new JobDTO(
            job.getJobId(),
            job.getJobTitle(),
            job.getCompany().getCompanyName()
        );
    }

}
