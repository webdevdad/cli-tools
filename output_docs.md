Data Version: 1.1

# Com/Example/Events

## UserCreatedEvent

Represents an event triggered when a new user is created.

| Property Name | Data Type | Description (from JavaDoc) | Annotations |
|---------------|-----------|----------------------------|-------------|
| userId        | String    | The unique identifier for the user. | @NotNull, @JsonProperty("userId") |
| email         | String    | The email address of the new user. | @NotNull |