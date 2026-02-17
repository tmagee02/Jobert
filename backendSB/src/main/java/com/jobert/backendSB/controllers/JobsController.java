package com.jobert.backendSB.controllers;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class JobsController {
    
    @GetMapping("/jobs")
    public String jobs(){
        //1. grab jobs within date range from db
        //2. create empty list of dicts for jobs
        //3. iterate through grabbed jobs
            //a. create a dict for that job with its jobId, jobUrl, company, and title
            //b. add dict to list
        //4. return Json of the list of job dicts
        
        return "jobs";
    }

    @GetMapping("jobInfo")
    public String jobInfo(){
        return "jobInfo";
    }
}
