package com.jobert.backendSB.Company;

import java.util.List;

import org.springframework.stereotype.Service;

@Service
public class CompanyService {

    private final CompanyRepository companyRepository;

    public CompanyService(CompanyRepository companyRepository){
        this.companyRepository = companyRepository;
    }

    public List<Company> getAllCompanies(){
        return companyRepository.findAll();
    }

    public Company getCompanyById(Integer companyId){
        return companyRepository.findById(companyId).orElseThrow();
    }

    public Company insertCompany(Company c){
        return companyRepository.save(c);
    }

}
