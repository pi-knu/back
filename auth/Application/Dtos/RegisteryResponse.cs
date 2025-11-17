namespace Application.Dtos;

public record RegisterResponse
    (
        string Email, 
        DateTime CreatedAt
    );