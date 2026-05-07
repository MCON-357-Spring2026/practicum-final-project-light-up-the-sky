package com.mcon152.pyro.web;

import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.GetMapping;

@RestController
public class PlannerController {

    @GetMapping("/")
    public String home() {
        return "Pyromusical Planner API is running!";
    }
}
