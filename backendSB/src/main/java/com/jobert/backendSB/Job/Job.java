package com.jobert.backendSB.Job;

import java.util.Objects;

import com.jobert.backendSB.Company.Company;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.ManyToOne;

@Entity
public class Job {

    @Id
    @GeneratedValue(strategy=GenerationType.IDENTITY)
    private Integer jobId;
    private String jobTitle;

    @ManyToOne
    private Company company;

    public Job(){}

    public Job(Integer id, String jobTitle, Company company){
        this.jobId = id;
        this.jobTitle = jobTitle;
        this.company = company;
    }

    public Integer getJobId(){
        return this.jobId;
    }

    public void setJobId(Integer id){
        this.jobId = id;
    }

    public String getJobTitle(){
        return this.jobTitle;
    }
    
    public void setJobTitle(String jobTitle){
        this.jobTitle = jobTitle;
    }

    public Company getCompany(){
        return this.company;
    }

    public void setCompany(Company company){
        this.company = company;
    }
    
    @Override
    public boolean equals(Object o){
        if (o == null || getClass() != o.getClass()) return false;
        Job that = (Job) o;
        return Objects.equals(jobId, that.jobId) && 
            Objects.equals(jobTitle, that.jobTitle) &&
            Objects.equals(company, that.company);
    }

    @Override
    public int hashCode(){
        return Objects.hash(jobId, jobTitle, company);
    }

    @Override
    public String toString(){
        return String.format("Job %d \n\tJob Title: %s \n\tCompany: %s",
            jobId, jobTitle, company.toString());
    }
}
