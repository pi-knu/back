using Domain.Entities;

namespace Application.Interfaces;

public interface IAuthService
{
    Task<Users> Register(string email, string password);
    Task<string?> Login(string email, string password);
    Task<string?> Refresh(string refreshToken);
}