package com.ridedemand.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import java.util.List;


public class Dtos {

    // ---- what the React app sends / receives ----
    public record PredictRequest(
            @NotNull Double latitude,
            @NotNull Double longitude,
            @NotBlank String vehicle,
            @NotBlank String time,     
            String date,                
            Double radiusKm) {          
    }

    public record AreaDemand(
            String area,
            double latitude,
            double longitude,
            double distanceKm,
            int expectedRides,
            double highDemandProbability) {
    }

    public record PredictResponse(List<AreaDemand> areas) {
    }

    public record UnmetDemandRequest(
            @NotBlank String area,
            @NotBlank String vehicleType) {
    }

    public record ObservationRequest(
            @NotBlank String driverId,
            @NotBlank String area,
            @NotBlank String vehicleType,
            boolean online,
            String rideOutcome,
            boolean consent) {
    }

    // ---- what we send to / get from the Python ML service ----
    public record MlItem(
            String area,
            String vehicle,
            int hour,
            @JsonProperty("day_of_week") int dayOfWeek,
            int month) {
    }

    public record MlRequest(List<MlItem> items) {
    }

    public record MlPrediction(
            @JsonProperty("expected_rides") int expectedRides,
            @JsonProperty("high_demand_probability") double highDemandProbability) {
    }

    public record MlResponse(List<MlPrediction> predictions) {
    }
}
