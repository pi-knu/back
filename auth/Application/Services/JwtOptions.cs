namespace Application.Services;

public class JwtOptions
{
    public string SecretKey { get; set; } = String.Empty;
    public int ExpireHours { get; set; } = 2;
}