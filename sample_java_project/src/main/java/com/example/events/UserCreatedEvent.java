package com.example.events;

import javax.validation.constraints.NotNull;
import com.fasterxml.jackson.annotation.JsonProperty;

/**
 * Represents an event triggered when a new user is created.
 */
public class UserCreatedEvent {

    /**
     * The unique identifier for the user.
     */
    @NotNull
    @JsonProperty("userId")
    private String userId;

    /**
     * The email address of the new user.
     */
    @NotNull
    private String email;

    // Constructor, getters, setters omitted for brevity
}
