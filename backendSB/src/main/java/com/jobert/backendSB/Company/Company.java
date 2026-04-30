package com.jobert.backendSB.Company;

import java.util.Objects;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;

@Entity
public class Company {

    @Id
    @GeneratedValue(strategy=GenerationType.IDENTITY)
    private Integer companyId;
    private String companyName;

    public Company(){

    }

    public Company(Integer id, String companyName){
        this.companyId = id;
        this.companyName = companyName;
    }

    public Integer getCompanyId(){
        return this.companyId;
    }

    public void setCompanyId(Integer id){
        this.companyId = id;
    }

    public String getCompanyName(){
        return this.companyName;
    }

    public void setCompanyName(String companyName){
        this.companyName = companyName;
    }

    @Override
    public boolean equals(Object o){
        if (o == null || getClass() != o.getClass()) return false;
        Company that = (Company) o;
        return Objects.equals(companyId, that.companyId) && Objects.equals(companyName, that.companyName);
    }

    @Override
    public int hashCode(){
        return Objects.hash(companyId, companyName);
    }

    @Override
    public String toString(){
        return String.format("Company Id: %d \nCompany Name: %s",
                this.companyId, this.companyName);
    }
}
