namespace Application.Services;

public class JwtOptions
{
    public string SecretKey { get; set; } = string.Empty;
    public int ExpiresHours { get; set; } 
    public string Issuer { get; set; } = string.Empty;
}