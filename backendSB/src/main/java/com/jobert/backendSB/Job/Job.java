package com.jobert.backendSB.Job;

import java.time.LocalDateTime;

import com.jobert.backendSB.Company.Company;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;

@Entity
public class Job {

    @Id
    @GeneratedValue(strategy=GenerationType.IDENTITY)
    private Integer jobId;
    private String jobUrl;
    private String title;

    @Column(columnDefinition="TEXT")
    private String jobDesc;
    private Integer minExperience;
    private Integer maxExperience;
    private LocalDateTime dateScraped;
    private LocalDateTime datePosted;
    private Integer minSalary;
    private Integer maxSalary;

    @ManyToOne
    @JoinColumn(name = "company_id")
    private Company company;
    
    public Job(){}

    public Job(Integer jobId, String jobUrl, String title, String jobDesc, Integer minExperience, Integer maxExperience,
            LocalDateTime dateScraped, LocalDateTime datePosted, Integer minSalary, Integer maxSalary,
            Company company) {
        this.jobId = jobId;
        this.jobUrl = jobUrl;
        this.title = title;
        this.jobDesc = jobDesc;
        this.minExperience = minExperience;
        this.maxExperience = maxExperience;
        this.dateScraped = dateScraped;
        this.datePosted = datePosted;
        this.minSalary = minSalary;
        this.maxSalary = maxSalary;
        this.company = company;
    }

    public Integer getJobId() {
        return jobId;
    }

    public void setJobId(Integer jobId) {
        this.jobId = jobId;
    }

    public String getJobUrl() {
        return jobUrl;
    }

    public void setJobUrl(String jobUrl) {
        this.jobUrl = jobUrl;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public String getJobDesc() {
        return jobDesc;
    }

    public void setJobDesc(String jobDesc) {
        this.jobDesc = jobDesc;
    }

    public Integer getMinExperience() {
        return minExperience;
    }

    public void setMinExperience(Integer minExperience) {
        this.minExperience = minExperience;
    }

    public Integer getMaxExperience() {
        return maxExperience;
    }

    public void setMaxExperience(Integer maxExperience) {
        this.maxExperience = maxExperience;
    }

    public LocalDateTime getDateScraped() {
        return dateScraped;
    }

    public void setDateScraped(LocalDateTime dateScraped) {
        this.dateScraped = dateScraped;
    }

    public LocalDateTime getDatePosted() {
        return datePosted;
    }

    public void setDatePosted(LocalDateTime datePosted) {
        this.datePosted = datePosted;
    }

    public Integer getMinSalary() {
        return minSalary;
    }

    public void setMinSalary(Integer minSalary) {
        this.minSalary = minSalary;
    }

    public Integer getMaxSalary() {
        return maxSalary;
    }

    public void setMaxSalary(Integer maxSalary) {
        this.maxSalary = maxSalary;
    }

    public Company getCompany() {
        return company;
    }

    public void setCompany(Company company) {
        this.company = company;
    }

    @Override
    public boolean equals(Object o){
        if (o == null || getClass() != o.getClass()) return false;
        Job that = (Job) o;
        return jobId != null && jobId.equals(that.jobId);
    }

    @Override
    public int hashCode(){
        return getClass().hashCode();
    }

    @Override
    public String toString(){
        return String.format("Job[\nId: %d\nCompany: %s\nTitle: %s\nURL: %s\n]",
            jobId, company.getCompanyName(), title, jobUrl);
    }

}
