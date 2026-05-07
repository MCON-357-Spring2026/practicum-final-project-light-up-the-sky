package com.mcon152.pyro;

import com.mcon152.pyro.model.Firework;
import com.mcon152.pyro.repository.FireworkRepository;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertFalse;

@SpringBootTest
class FireworkDatabaseTest {

    @Autowired
    private FireworkRepository fireworkRepository;

    @Test
    void testFireworksArePresent() {
        // 1. Ask the database for everything it has
        List<Firework> fireworks = (List<Firework>) fireworkRepository.findAll();

        // 2. Print the results to the console so we can see it with our eyes
        System.out.println("========================================");
        System.out.println("DATABASE CHECK: Found " + fireworks.size() + " fireworks.");
        System.out.println("========================================");

        // 3. This is the "Pass/Fail" check
        assertFalse(fireworks.isEmpty(), "Error: The database is empty!");
    }
}