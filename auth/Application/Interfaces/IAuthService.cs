using Application.Dtos;
using Domain.Entities;

namespace Application.Interfaces;

public interface IAuthService
{
    Task<RegisterResponse> RegisterAsync(string email, string password);
    Task<LoginResponse> LoginAsync(string email, string password);
    Task<RefreshTokenResponse> RefreshAsync(string refreshToken);
}