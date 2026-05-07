package com.mcon152.pyro;

import com.mcon152.pyro.service.FireworkService;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;

@SpringBootApplication
public class PyromusicalPlannerApplication {

    public static void main(String[] args) {
        SpringApplication.run(PyromusicalPlannerApplication.class, args);
    }

/*    @Bean
    public CommandLineRunner demo(FireworkService fireworkService) {
        return (args) -> {
            // REPLACE THE PATH BELOW with your actual path!
            // Note: Use forward slashes / even on Windows to avoid errors
            String path = "C:/Users/student/Downloads/fireworks.csv";

            System.out.println("Starting import...");
            fireworkService.importFromCsv(path);
        };
    }*/
}
