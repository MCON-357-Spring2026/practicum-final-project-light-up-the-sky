package com.mcon152.pyro.service;

import com.mcon152.pyro.model.Firework;
import com.mcon152.pyro.repository.FireworkRepository;
import com.opencsv.bean.CsvToBeanBuilder;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.io.FileReader;
import java.util.List;

@Service
public class FireworkService {

    @Autowired
    private FireworkRepository fireworkRepository;

    public void importFromCsv(String filePath) {
        try (FileReader reader = new FileReader(filePath)) {
            List<Firework> fireworks = new CsvToBeanBuilder<Firework>(reader)
                    .withType(Firework.class)
                    .build()
                    .parse();

            fireworkRepository.saveAll(fireworks);
            System.out.println("--- SUCCESS ---");
            System.out.println("Imported " + fireworks.size() + " fireworks into the database!");
        } catch (Exception e) {
            System.err.println("--- ERROR ---");
            System.err.println("Could not read the CSV file. Make sure the path is correct.");
            e.printStackTrace();
        }
    }
}