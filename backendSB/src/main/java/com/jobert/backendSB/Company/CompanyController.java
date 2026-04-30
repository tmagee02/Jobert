package com.jobert.backendSB.Company;

import java.util.List;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/companies")
public class CompanyController {

    private final CompanyService companyService;

    public CompanyController(CompanyService companyService){
        this.companyService = companyService;
    }

    @GetMapping
    public List<Company> getCompanies(){
        return companyService.getAllCompanies();
    }

    @PostMapping
    public Company insertCompany(@RequestBody Company c){
        return companyService.insertCompany(c);
    }
}
