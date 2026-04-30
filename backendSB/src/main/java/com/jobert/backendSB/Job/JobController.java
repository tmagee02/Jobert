package com.jobert.backendSB.Job;

import java.util.List;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/jobs")
public class JobController {

    private final JobService jobService;

    public JobController(JobService jobService){
        this.jobService = jobService;
    }

    //need to change to DTO
    @GetMapping
    public List<JobDTO> getJobs(){
        /*
            1. Get the following from the client request:
                offset (query start), jobCount (i forget),
                desired companies, salary, experience  
            2. filter by 30 days
            3. filter by desired companies
            4. filter by desired salary
            5. filter by desired experience
            6. order filtered jobs by most recent first and
                only whitelist the ones in desired range
            7. make a list of hashmaps with each jobs info
            8. return json response with list and total jobs
        */
       return jobService.getAllJobs();
    }

    @GetMapping("{jobId}")
    public Job getJobInfo(@PathVariable Integer jobId){
        /*
            1. get job from db by id if exists
            2. put into json object?
            3. return json response
        */
        return null;
    }

    @PostMapping
    public JobDTO insertJob(@RequestBody InsertJobRequest j){
        return jobService.insertJob(j);
    }
}
