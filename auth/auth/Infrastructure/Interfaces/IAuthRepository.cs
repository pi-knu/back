using Domain.Entities;

namespace Application.Interfaces;

public interface IAuthRepository
{
    Task AddUserAsync(Users user);
    Task<Users?> GetUserByEmailAsync(string email);
}