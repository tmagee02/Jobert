package com.jobert.backendSB.Job;

import java.util.List;

import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.jobert.backendSB.Job.dto.GetJobsResponse;
import com.jobert.backendSB.Job.dto.JobDetailsDTO;

@CrossOrigin(origins="http://localhost:5173")
@RestController
@RequestMapping("/jobs")
public class JobController {

    private final JobService jobService;

    public JobController(JobService jobService){
        this.jobService = jobService;
    }

    @GetMapping
    public GetJobsResponse getJobs(
        @RequestParam(defaultValue = "0") Integer offset,
        @RequestParam(defaultValue = "20") Integer jobCount,
        @RequestParam(required = false) List<String> companies,
        @RequestParam(required = false) Integer salary,
        @RequestParam(required = false) Integer experience
    ){ 
       return jobService.getFilteredJobs(
            offset, 
            jobCount, 
            companies, 
            salary, 
            experience
        );
    }

    @GetMapping("{jobId}")
    public JobDetailsDTO getJobInfo(@PathVariable Integer jobId){
        return jobService.getJobDetails(jobId);
    }

}
