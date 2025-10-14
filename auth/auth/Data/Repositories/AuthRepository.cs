using Data.Entities;
using Microsoft.EntityFrameworkCore;

namespace Data.Repositories;

public class AuthRepository(DataContext dataContext)
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
}