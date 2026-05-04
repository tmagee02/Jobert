package com.jobert.backendSB.Job.dto;

import java.time.LocalDateTime;

public record JobDTO(
    Integer id,
    String jobUrl,
    String companyName,
    String jobTitle,
    Integer minExperience,
    Integer maxExperience,
    Integer minSalary,
    Integer maxSalary,
    LocalDateTime dateScraped
) {

}
