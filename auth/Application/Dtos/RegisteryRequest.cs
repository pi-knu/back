namespace Application.Dtos;

public record RegisteryRequest
    (
        string Email,
        string Password
    );