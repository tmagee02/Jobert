package com.jobert.backendSB.Job.mapper;

import java.util.function.Function;

import org.springframework.data.domain.Page;
import org.springframework.stereotype.Component;

import com.jobert.backendSB.Job.dto.GetJobsResponse;
import com.jobert.backendSB.Job.dto.JobDTO;

@Component
public class GetJobsResponseMapper implements Function<Page<JobDTO>, GetJobsResponse> {

    @Override
    public GetJobsResponse apply(Page<JobDTO> page) {
        return new GetJobsResponse(
            page.getContent(),
            page.getTotalElements()
        );
    }

}
