package com.jobert.backendSB;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@SpringBootApplication
@RestController
public class BackendSbApplication {

	public static void main(String[] args) {
		SpringApplication.run(BackendSbApplication.class, args);
	}

	@GetMapping
	public String test(){
		return "Hello tim - this is the first jobert SB endpoint!";
	}

}
