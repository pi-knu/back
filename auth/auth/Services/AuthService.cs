using Data.Entities;
using Data.Repositories;

namespace Services;

// TODO: make map to dto in controller

public class AuthService(AuthRepository repository)
{
    public async Task<Users> Register(string email, string password)
    {
        var user = new Users
        {
            Email = email,
            
            // TODO: make hash password
            Password = password,
            
            CreatedAt = DateTime.Now
        };
        
        return user;
    }
    
    public async Task<string?> Login(string email, string password)
    {
        var user = await repository.GetUserByEmailAsync(email);
        
        if(user == null) return null;
        
        // TODO: make verify by password, generate jwt token
        
        return password == user.Password ? user.Email : null;
    }
}