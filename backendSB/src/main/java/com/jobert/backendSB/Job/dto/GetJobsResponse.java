package com.jobert.backendSB.Job.dto;

import java.util.List;

public record GetJobsResponse(
    List<JobDTO> jobList,
    Long totalJobs
) {

}
