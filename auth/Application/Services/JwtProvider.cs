using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;
using System.Security.Cryptography;
using System.Text;
using Application.Interfaces;
using Domain.Entities;
using Microsoft.Extensions.Options;
using Microsoft.IdentityModel.Tokens;

namespace Application.Services;

public class JwtProvider : IJwtProvider
{
    private readonly JwtOptions _options;
    public JwtProvider(IOptions<JwtOptions> jwtOtions)
    {
        _options = jwtOtions.Value;
    }

    public string GenerateToken(Users user)
    {
        Claim[] claims = [new("userId", user.Id.ToString())];
        
        var signingCredentials = new SigningCredentials
        (
            new SymmetricSecurityKey(Encoding.ASCII.GetBytes(_options.SecretKey)), 
            SecurityAlgorithms.HmacSha256Signature);
        
        var token = new JwtSecurityToken
        (
            claims: claims,
            signingCredentials: signingCredentials,
            expires: DateTime.UtcNow.AddHours(_options.ExpireHours)
        );
        
        var tokenString = new JwtSecurityTokenHandler().WriteToken(token);
        
        return tokenString;
    }

    public string GenerateRefreshToken()
    {
        var randomBytes = new byte[32];
        using var rng = RandomNumberGenerator.Create();
        rng.GetBytes(randomBytes);
        return Convert.ToBase64String(randomBytes);
    }
}
