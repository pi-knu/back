namespace Application.Dtos;

public record LoginResponse
    (
        string AccessToken,
        string RefreshToken
    );