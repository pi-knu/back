using Application.Dtos;
using Application.Interfaces;
using Domain.Entities;
namespace Application;

// TODO: make map to dto in controller

public class AuthService(IAuthRepository repository, IPasswordHasher hasher, IJwtProvider provider):IAuthService
{
    private static readonly Dictionary<Guid, string> _tokenCache = new();

    public async Task<RegisterResponse> RegisterAsync(string email, string password)
    {
        var existingUser = await repository.GetUserByEmailAsync(email);
        if (existingUser is not null)
            throw new InvalidOperationException("User with this email already exists.");
        
        if (!IsValidEmail(email))
            throw new ArgumentException("Invalid email format.");
        
        if (string.IsNullOrWhiteSpace(password) || password.Length < 6)
            throw new ArgumentException("Password must be at least 6 characters long.");
        
        var hashedPassword = hasher.HashPassword(password);
        
        var user = new Users
        {
            Email = email,
            Password = hashedPassword,
            CreatedAt = DateTime.UtcNow
        };

        await repository.AddUserAsync(user);
        
        return new RegisterResponse(user.Email, user.CreatedAt);
    }

    private bool IsValidEmail(string email)
    {
        try
        {
            var addr = new System.Net.Mail.MailAddress(email);
            return addr.Address == email;
        }
        catch
        {
            return false;
        }
    }
    public async Task<string?> Login(string email, string password)
    {
        var user = await repository.GetUserByEmailAsync(email);
        
        if(user == null) return null;
        
       var result = hasher.VerifyHashedPassword(user.Password, password);
       
       if(!result) 
           throw new UnauthorizedAccessException("Invalid password");
        
       var token = provider.GenerateToken(user);
       var refreshToken = provider.GenerateRefreshToken();
       
       _tokenCache[user.Id] = refreshToken;

       
       return token;
       // TODO: implement dto to controller
    }
    
    public async Task<string?> Refresh(string refreshToken)
    {
        var userEntry = _tokenCache.FirstOrDefault(x => x.Value == refreshToken);
        if (userEntry.Key == Guid.Empty)
            throw new UnauthorizedAccessException("Invalid refresh token");

        var userId = userEntry.Key;
        var user = new Users { Id = userId }; 

        var newAccessToken = provider.GenerateToken(user);
        var newRefreshToken = provider.GenerateRefreshToken();

        _tokenCache[userId] = newRefreshToken;

        return newAccessToken;
    }
}