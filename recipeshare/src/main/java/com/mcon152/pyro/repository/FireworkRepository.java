package com.mcon152.pyro.repository;

import com.mcon152.pyro.model.Firework;
import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface FireworkRepository extends CrudRepository<Firework, Long> {
    // This looks empty, but it secretly has "save()", "findAll()", and "delete()" built-in!
}