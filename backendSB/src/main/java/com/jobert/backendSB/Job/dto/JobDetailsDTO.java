package com.jobert.backendSB.Job.dto;

import java.time.LocalDateTime;

public record JobDetailsDTO(
    String companyName,
    String jobUrl,
    String jobTitle,
    String jobDesc,
    Integer minExperience,
    Integer maxExperience,
    Integer minSalary,
    Integer maxSalary,
    LocalDateTime dateScraped
) {

}
