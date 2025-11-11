namespace Application.Dtos;

public record RefreshTokenResponse
    (
        string AccessToken,
        string RefreshToken
    );