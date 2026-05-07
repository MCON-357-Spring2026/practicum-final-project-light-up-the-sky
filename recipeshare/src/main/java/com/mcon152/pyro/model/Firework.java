package com.mcon152.pyro.model;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;

@Entity
public class Firework {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String name;
    private Double duration; // How many seconds it lasts
    private String pace;     // "Slow", "Medium", or "Fast"

    // Default constructor (required by JPA)
    public Firework() {}

    // Constructor for easy creation
    public Firework(String name, Double duration, String pace) {
        this.name = name;
        this.duration = duration;
        this.pace = pace;
    }

    // Getters and Setters (This allows the app to read/write the data)
    public Long getId() { return id; }
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public Double getDuration() { return duration; }
    public void setDuration(Double duration) { this.duration = duration; }
    public String getPace() { return pace; }
    public void setPace(String pace) { this.pace = pace; }
}