package com.jobert.backendSB.Job;

import java.util.List;

import org.springframework.stereotype.Service;

import com.jobert.backendSB.Company.Company;
import com.jobert.backendSB.Company.CompanyRepository;

@Service
public class JobService {

    private final JobRepository jobRepository;
    private final CompanyRepository companyRepository;
    private final JobDTOMapper mapper;

    public JobService(JobRepository jobRepository, CompanyRepository companyRepository, JobDTOMapper mapper){
        this.jobRepository = jobRepository;
        this.companyRepository = companyRepository;
        this.mapper = mapper;
    }

    public List<JobDTO> getAllJobs(){
        return jobRepository.findAll()
            .stream()
            .map(mapper)
            .toList();
    }

    public JobDTO insertJob(InsertJobRequest j){
        Company company = companyRepository.findById(j.companyId()).orElseThrow();
        Job createdJob = new Job();
        createdJob.setJobTitle(j.jobTitle());
        createdJob.setCompany(company); 
        Job savedJob = jobRepository.save(createdJob);
        System.out.println(savedJob.toString());
        return mapper.apply(savedJob);
    }

}
