using Application.Dtos;
using Domain.Entities;

namespace Application.Interfaces;

public interface IAuthService
{
    Task<RegisterResponse> RegisterAsync(string email, string password);
    Task<string?> Login(string email, string password);
    Task<string?> Refresh(string refreshToken);
}