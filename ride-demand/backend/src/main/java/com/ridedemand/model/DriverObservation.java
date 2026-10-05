package com.ridedemand.model;

import jakarta.persistence.*;
import java.time.LocalDateTime;

// one periodic snapshot from a driver who agreed to share data
@Entity
@Table(name = "driver_observations")
public class DriverObservation {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String driverId;
    private String area;
    private String vehicleType;
    private boolean online;
    private String rideOutcome;   // COMPLETED, Cancelled etc
    private LocalDateTime observedAt;

    public DriverObservation() {}

    public DriverObservation(String driverId, String area, String vehicleType, boolean online, String rideOutcome) {
        this.driverId = driverId;
        this.area = area;
        this.vehicleType = vehicleType;
        this.online = online;
        this.rideOutcome = rideOutcome;
        this.observedAt = LocalDateTime.now();
    }

    public Long getId() { return id; }
    public String getDriverId() { return driverId; }
    public String getArea() { return area; }
    public String getVehicleType() { return vehicleType; }
    public boolean isOnline() { return online; }
    public String getRideOutcome() { return rideOutcome; }
    public LocalDateTime getObservedAt() { return observedAt; }
}
