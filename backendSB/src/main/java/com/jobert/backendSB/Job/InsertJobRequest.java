package com.jobert.backendSB.Job;

public record InsertJobRequest(
    String jobTitle,
    Integer companyId
) {

}
