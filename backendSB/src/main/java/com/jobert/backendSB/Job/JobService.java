package com.jobert.backendSB.Job;

import java.time.LocalDateTime;
import java.time.ZoneOffset;
import java.util.List;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;

import com.jobert.backendSB.Job.dto.GetJobsResponse;
import com.jobert.backendSB.Job.dto.JobDTO;
import com.jobert.backendSB.Job.dto.JobDetailsDTO;
import com.jobert.backendSB.Job.mapper.GetJobsResponseMapper;
import com.jobert.backendSB.Job.mapper.JobDTOMapper;
import com.jobert.backendSB.Job.mapper.JobDetailsDTOMapper;


@Service
public class JobService {

    private final JobRepository jobRepository;
    private final JobDTOMapper jobMapper;
    private final GetJobsResponseMapper getJobsResponseMapper;
    private final JobDetailsDTOMapper jobDetailsMapper;

    public JobService(
        JobRepository jobRepository, 
        JobDTOMapper jobMapper, 
        GetJobsResponseMapper getJobsResponseMapper,
        JobDetailsDTOMapper jobDetailsMapper 
    ){
        this.jobRepository = jobRepository;
        this.jobMapper = jobMapper;
        this.getJobsResponseMapper = getJobsResponseMapper;
        this.jobDetailsMapper = jobDetailsMapper;
    }

    public GetJobsResponse getFilteredJobs(
        Integer offset, 
        Integer jobCount, 
        List<String> companies,
        Integer salary,
        Integer experience
    ){
        LocalDateTime thirtyDays = LocalDateTime.now(ZoneOffset.UTC).minusDays(30); 
        int curPage = offset / jobCount;
        Pageable pageable = PageRequest.of(curPage, jobCount);
        Page<JobDTO> page = jobRepository.filterJobs(
                thirtyDays, 
                companies, 
                salary, 
                experience, 
                pageable
            )
            .map(jobMapper);
        return getJobsResponseMapper.apply(page);
    }

    public JobDetailsDTO getJobDetails(Integer jobId){
        return jobDetailsMapper.apply(
            jobRepository.findById(jobId).orElseThrow()
        );
    }

}
