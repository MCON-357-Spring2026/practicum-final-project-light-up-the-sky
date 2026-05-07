package com.mcon152.pyro.model;

import com.opencsv.bean.CsvBindByName;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;

@Entity
public class Firework {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @CsvBindByName(column = "name")
    private String name;

    @CsvBindByName(column = "duration")
    private Double duration;

    @CsvBindByName(column = "pace")
    private String pace;

    // Default constructor (Required for JPA and OpenCSV)
    public Firework() {}

    // Constructor for creating fireworks manually
    public Firework(String name, Double duration, String pace) {
        this.name = name;
        this.duration = duration;
        this.pace = pace;
    }

    // Getters and Setters
    public Long getId() { return id; }

    public String getName() { return name; }
    public void setName(String name) { this.name = name; }

    public Double getDuration() { return duration; }
    public void setDuration(Double duration) { this.duration = duration; }

    public String getPace() { return pace; }
    public void setPace(String pace) { this.pace = pace; }
}