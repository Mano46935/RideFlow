package com.ridedemand.controller;

import com.ridedemand.dto.Dtos.ObservationRequest;
import com.ridedemand.dto.Dtos.RideFoundRequest;
import com.ridedemand.dto.Dtos.UnmetDemandRequest;
import com.ridedemand.service.DataCollectionService;
import jakarta.validation.Valid;
import java.util.Map;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api")
public class DataCollectionController {

    private final DataCollectionService service;

    public DataCollectionController(DataCollectionService service) {
        this.service = service;
    }

    @PostMapping("/reports/unmet-demand")
    public ResponseEntity<Map<String, Object>> reportUnmetDemand(
            @RequestHeader("X-User-Id") String userId,
            @Valid @RequestBody UnmetDemandRequest request) {

        var saved = service.saveReport(userId, request);
        return ResponseEntity.status(HttpStatus.CREATED)
                .body(Map.of("id", saved.getId(), "status", saved.getStatus()));
    }

    @PostMapping("/observations")
    public ResponseEntity<Map<String, Object>> addObservation(@Valid @RequestBody ObservationRequest request) {
        var saved = service.saveObservation(request);
        return ResponseEntity.status(HttpStatus.CREATED).body(Map.of("id", saved.getId()));
    }

    @PostMapping("/observations/ride-found")
    public ResponseEntity<Map<String, Object>> reportRideFound(@Valid @RequestBody RideFoundRequest request) {
        var saved = service.saveRideFound(request);
        return ResponseEntity.status(HttpStatus.CREATED).body(Map.of("id", saved.getId()));
    }
}
