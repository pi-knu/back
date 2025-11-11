using Application.Interfaces;
using Domain.Entities;
using Infrastructure.Data;
using Microsoft.EntityFrameworkCore;

namespace Infrastructure.Repositories;

public class AuthRepository(DataContext dataContext) : IAuthRepository
{
    public async Task AddUserAsync(Users user)
    {
        await dataContext.Users.AddAsync(user);
        await dataContext.SaveChangesAsync();
    }

    public async Task<Users?> GetUserByEmailAsync(string email)
    {
        return await dataContext.Users
            .FirstOrDefaultAsync(u => u.Email == email);
    }

    public async Task<Users?> GetUserByIdAsync(Guid userId)
    {
        return await dataContext.Users
            .FirstOrDefaultAsync(u=> u.Id == userId);
    }
}

