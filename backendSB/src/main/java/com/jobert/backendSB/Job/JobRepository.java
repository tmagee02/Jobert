package com.jobert.backendSB.Job;

import java.time.LocalDateTime;
import java.util.List;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;

public interface JobRepository extends JpaRepository<Job, Integer>{
    
    @Query("""
    SELECT j 
    FROM Job j
    JOIN j.company c
    WHERE j.dateScraped >= :thirtyDays
    AND (
            :companies IS NULL OR 
            c.companyName IN :companies
        )
    AND (
            :salary IS NULL OR 
            j.maxSalary IS NULL OR 
            j.maxSalary >= :salary
        )
    AND (
            :experience IS NULL OR 
            j.minExperience IS NULL OR 
            (
                j.maxExperience IS NULL AND 
                j.minExperience <= :experience
            ) OR
            (
                j.minExperience <= :experience AND 
                j.maxExperience >= :experience
            )
        )
    ORDER BY j.id DESC
    """)
    public Page<Job> filterJobs(
        LocalDateTime thirtyDays,
        List<String> companies,
        Integer salary,
        Integer experience,
        Pageable pageable
    );

}
